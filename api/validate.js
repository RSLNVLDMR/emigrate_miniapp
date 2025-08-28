// /api/validate.js — Serverless (Node.js) на Vercel
// Принимает: { docType: "insurance", file: { dataUrl, filename, mime } }
// Возвращает: { ok, issues, hints, extracted }

import fs from "fs/promises";

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end("Method Not Allowed");
  try {
    const { docType, file } = await readJson(req);
    if (!docType || !file?.dataUrl) {
      return res.status(400).json({ error: "docType and file are required" });
    }

    const rules = JSON.parse(
      await fs.readFile("templates/validation/rules.json", "utf8")
    );
    const cfg = rules[docType];
    if (!cfg) return res.status(400).json({ error: `Unknown docType: ${docType}` });

    // 1) Сбор входа для модели: инструкция + контент файла (текст из PDF или изображение)
    const userParts = [
      {
        type: "input_text",
        text:
          "Extract the following fields from the Polish insurance document. " +
          "If a field is missing, set it to an empty string. " +
          "Fields: " + Object.keys(buildExtractionSchema(docType).properties).join(", ")
      }
    ];

    if (file.mime === "application/pdf") {
      // Пытаемся извлечь текст из PDF
      const buf = Buffer.from(file.dataUrl.split(",")[1], "base64");
      try {
        const pdfParse = (await import("pdf-parse")).default;
        const pdf = await pdfParse(buf);
        if (pdf?.text?.trim()) {
          userParts.push({
            type: "input_text",
            text: `PDF text (may be partial):\n${pdf.text.slice(0, 45000)}`
          });
        } else {
          // Если PDF — скан без текста: сообщаем пользователю (модель не увидит изображение из PDF)
          // В проде можно добавить конвертацию PDF→images (например, через poppler/imagemagick).
        }
      } catch {
        // тихо продолжаем; без текста модель всё равно вернёт пустые поля — их поймает валидация
      }
    } else {
      // Фото/скан
      userParts.push({ type: "input_image", image_url: file.dataUrl });
    }

    const extractionSchema = buildExtractionSchema(docType);

    const body = {
      model: "gpt-4o-mini",
      input: [{ role: "user", content: userParts }],
      response_format: { type: "json_schema", json_schema: { name: "Extracted", schema: extractionSchema } }
    };

    const r = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    if (!r.ok) {
      return res.status(500).json({ error: "OpenAI error", detail: await r.text() });
    }
    const data = await r.json();
    const extracted = safeJson(data.output_text) || {};

    // 2) Жёсткая проверка полей кодом (required + patterns + логика дат)
    const { issues, hints } = validateExtracted(extracted, cfg);

    return res.json({
      ok: issues.length === 0,
      issues,
      hints,
      extracted
    });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ error: "Server error" });
  }
}

function buildExtractionSchema(docType) {
  if (docType === "insurance") {
    return {
      type: "object",
      additionalProperties: false,
      properties: {
        insurer_name: { type: "string" },
        policy_number: { type: "string" },
        insured_name: { type: "string" },
        id_number: { type: "string" },
        valid_from: { type: "string" },     // YYYY-MM-DD
        valid_to: { type: "string" },       // YYYY-MM-DD
        coverage_summary: { type: "string" },
        signatures_present: { type: "boolean" },
        stamp_present: { type: "boolean" }
      },
      required: []
    };
  }
  // можно расширять для других docType при необходимости
  return { type: "object", additionalProperties: true, properties: {} };
}

function validateExtracted(ex, cfg) {
  const issues = [];
  const hints = [];

  // required
  for (const f of (cfg.requiredFields || [])) {
    if (ex[f] === undefined || (typeof ex[f] === "string" && !ex[f].trim())) {
      issues.push(`Отсутствует обязательное поле: ${f}`);
    }
  }

  // patterns
  for (const [f, pattern] of Object.entries(cfg.patterns || {})) {
    const v = (ex[f] ?? "").toString();
    if (v && !new RegExp(pattern).test(v)) {
      issues.push(`Поле ${f} не соответствует формату (${pattern})`);
    }
  }

  // Доп. логика дат для страховки
  if (cfg.displayName === "Ubezpieczenie medyczne") {
    const from = Date.parse(ex.valid_from);
    const to = Date.parse(ex.valid_to);
    if (!Number.isNaN(from) && !Number.isNaN(to)) {
      if (to < from) issues.push("Дата окончания полиса раньше даты начала");
      const today = new Date(); today.setHours(0,0,0,0);
      if (to < +today) issues.push("Срок действия полиса истёк");
    }
    if (!ex.coverage_summary || ex.coverage_summary.length < 5) {
      hints.push("Покрытия не распознаны: проверьте, что в полисе указаны ключевые разделы (неотложка/стационар/амбулаторное)");
    }
  }

  hints.push(...(cfg.redFlagHints || []));
  return { issues, hints };
}

function safeJson(s) { try { return JSON.parse(s); } catch { return null; } }

async function readJson(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}
