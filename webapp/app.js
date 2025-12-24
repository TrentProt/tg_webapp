const tg = window.Telegram.WebApp;
const initData = tg.initData;
const API_URL = "https://7a5bdf1fff3d93.lhr.life"; // сюда URL FastAPI (public через ngrok/Cloudflare)

async function loadList() {
  const res = await fetch(`${API_URL}/containers?initData=${initData}`);
  if (!res.ok) {
    console.error("Ошибка загрузки списка", res.status);
    return;
  }
  const data = await res.json();
  const list = document.getElementById("list");

  data.forEach(c => {
    const div = document.createElement("div");
    div.innerHTML = `
      <h3>${c.name}</h3>
      <img src="${c.images[0]}" width="200"/>
      <button onclick="openItem(${c.id})">Открыть</button>
    `;
    list.appendChild(div);
  });
}

function openItem(id) {
  window.location.href = `/static/item.html?id=${id}`;
}

async function loadItem() {
  const id = new URLSearchParams(window.location.search).get("id");
  if (!id) return;

  const res = await fetch(`${API_URL}/container/${id}?initData=${initData}`);
  if (!res.ok) {
    console.error("Ошибка загрузки контейнера", res.status);
    return;
  }
  const c = await res.json();
  const itemDiv = document.getElementById("item");
  itemDiv.innerHTML = `
    <h2>${c.name}</h2>
    <p>${c.description}</p>
    <p>Цена: ${c.price}$</p>
    ${c.images.map(i => `<img src="${i}" width="200"/>`).join("")}
  `;
}

// Автозагрузка
if (document.getElementById("list")) loadList();
if (document.getElementById("item")) loadItem();

