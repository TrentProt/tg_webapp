const tg = window.Telegram.WebApp;
const API_URL = "https://e43fb6f60393d2.lhr.life";

tg.ready();

async function loadList() {
  console.log("loadList вызван!");

  if (!tg.initData) {
    console.error("initData отсутствует!");
    showError("Ошибка: initData отсутствует");
    return;
  }

  console.log("initData:", tg.initData);

  // URL-кодируем initData для передачи в GET
  const encodedInitData = encodeURIComponent(tg.initData);
  const url = `${API_URL}/containers?initData=${encodedInitData}`;

  console.log("Отправляю GET запрос на:", url);

  try {
    const res = await fetch(url, {
      method: "GET",
      headers: {
        "Accept": "application/json"
      }
    });

    console.log("Статус ответа:", res.status);

    if (!res.ok) {
      const errorText = await res.text();
      console.error("Ошибка загрузки списка", res.status, errorText);
      showError(`Ошибка ${res.status}: ${errorText}`);
      return;
    }

    const data = await res.json();
    console.log("Получены данные:", data);

    displayContainers(data);

  } catch (error) {
    console.error("Ошибка fetch:", error);
    showError(`Ошибка сети: ${error.message}`);
  }
}

async function openItem(id) {
  console.log("Открываем элемент:", id);

  if (!tg.initData) {
    console.error("initData отсутствует при открытии элемента!");
    alert("Ошибка: initData отсутствует");
    return;
  }

  const encodedInitData = encodeURIComponent(tg.initData);
  const url = `${API_URL}/container/${id}?initData=${encodedInitData}`;

  console.log("Загружаем контейнер с URL:", url);

  try {
    const res = await fetch(url, {
      method: "GET",
      headers: {
        "Accept": "application/json"
      }
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error("Ошибка загрузки контейнера", res.status, errorText);
      alert(`Ошибка загрузки: ${errorText}`);
      return;
    }

    const container = await res.json();
    console.log("Получен контейнер:", container);

    // Показываем детали контейнера на этой же странице
    displayContainerDetails(container);

  } catch (error) {
    console.error("Ошибка загрузки контейнера:", error);
    alert(`Ошибка сети: ${error.message}`);
  }
}

function displayContainers(containers) {
  const list = document.getElementById("list");
  if (!list) {
    console.error("Элемент #list не найден!");
    return;
  }

  if (containers.length === 0) {
    list.innerHTML = "<p>Нет контейнеров</p>";
    return;
  }

  list.innerHTML = "";
  containers.forEach(c => {
    const div = document.createElement("div");
    div.className = "container-item";
    div.style.border = "1px solid #ccc";
    div.style.borderRadius = "8px";
    div.style.padding = "15px";
    div.style.margin = "10px 0";
    div.style.backgroundColor = "#f9f9f9";

    div.innerHTML = `
      <h3>${c.name || 'Без названия'}</h3>
      ${c.description ? `<p>${c.description}</p>` : ''}
      ${c.images && c.images[0] ? `<img src="${c.images[0]}" width="200" style="border-radius: 4px; margin: 10px 0;">` : ''}
      <div>
        <button onclick="openItem(${c.id})" style="padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
          Открыть детали
        </button>
      </div>
    `;
    list.appendChild(div);
  });

  console.log("Список отображен!");
}

function displayContainerDetails(container) {
  const list = document.getElementById("list");
  if (!list) return;

  list.innerHTML = `
    <div style="max-width: 600px; margin: 0 auto;">
      <button onclick="loadList()" style="margin-bottom: 20px; padding: 8px 16px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">
        ← Назад к списку
      </button>

      <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2>${container.name || 'Без названия'}</h2>
        <p><strong>ID:</strong> ${container.id}</p>
        ${container.description ? `<p><strong>Описание:</strong> ${container.description}</p>` : ''}

        ${container.images && container.images.length > 0 ? `
          <h3>Изображения (${container.images.length}):</h3>
          <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
            ${container.images.map(img => `
              <img src="${img}" width="150" style="border-radius: 4px;">
            `).join('')}
          </div>
        ` : '<p>Нет изображений</p>'}

        <p style="margin-top: 20px; color: #666; font-size: 12px;">
          ID контейнера: ${container.id}
        </p>
      </div>
    </div>
  `;
}

function showError(message) {
  const list = document.getElementById("list");
  if (list) {
    list.innerHTML = `
      <div style="color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 15px; margin: 20px 0;">
        <h3>Ошибка</h3>
        <p>${message}</p>
        <button onclick="location.reload()" style="padding: 8px 16px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer;">
          Обновить страницу
        </button>
      </div>
    `;
  }
}

// Запускаем при загрузке
document.addEventListener('DOMContentLoaded', () => {
  console.log("DOM загружен");

  // Проверяем, есть ли initData
  if (tg.initData) {
    console.log("initData уже есть, запускаем loadList");
    loadList();
  } else {
    console.log("initData еще нет, ждем...");
    // Ждем немного и проверяем снова
    setTimeout(() => {
      if (tg.initData) {
        loadList();
      } else {
        showError("Не удалось получить данные авторизации. Пожалуйста, перезапустите приложение.");
      }
    }, 1000); // Ждем 1 секунду

    // Также можно подписаться на события WebApp
    tg.onEvent('viewportChanged', function() {
      console.log("viewportChanged, проверяем initData");
      if (tg.initData) {
        loadList();
      }
    });

    tg.onEvent('themeChanged', function() {
      console.log("themeChanged, проверяем initData");
      if (tg.initData) {
        loadList();
      }
    });
  }
});

// Делаем функции глобальными для обработчиков onclick
window.loadList = loadList;
window.openItem = openItem;
window.showError = showError;
window.displayContainers = displayContainers;
window.displayContainerDetails = displayContainerDetails;
