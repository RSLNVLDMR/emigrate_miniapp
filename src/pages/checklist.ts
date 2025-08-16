const items = [
  { href: "/questionnaire", title: "Анкета (wniosek)", desc: "Заполнить шаблон, предпросмотр и ✎-правка" },
  { href: "/photos", title: "Фотографии 3.5×4.5", desc: "Загрузите фото — проверим автоматически" },
  { href: "/oplata-skarbowa", title: "Opłata skarbowa", desc: "Реквизиты и отметка об оплате" },
  { href: "/upload-contract", title: "Договор (UoP/UoD/B2B)", desc: "Проверка подписей, дат, NIP" },
  { href: "/zalacznik-pracodawcy", title: "Załącznik od pracodawcy", desc: "Шаблон → подпись/печать → загрузка" },
  { href: "/umowa-meldunek", title: "Umowa najmu / Meldunek", desc: "Проверим адрес, сроки, подписи" },
  { href: "/zaswiadczenie-uczelnia", title: "Zaświadczenie z uczelni", desc: "Для студентов — загрузите справку" },
  { href: "/srodki-finansowe", title: "Финансовые средства", desc: "Выписка: сумма/дата/реквизиты" },
  { href: "/ubezpieczenie", title: "Страховка (Private/NFZ/ZUS)", desc: "Проверим срок действия" },
  { href: "/find-slot", title: "Запись в ужонд", desc: "Найти и забронировать слот" }
];

const list = document.getElementById("list")!;
list.innerHTML = items
  .map(
    (i) => `
    <a class="card" href="${i.href}" style="display:block;text-decoration:none;color:inherit">
      <div style="font-weight:600">${i.title}</div>
      <div style="color:#666;font-size:14px">${i.desc}</div>
    </a>`
  )
  .join("");
