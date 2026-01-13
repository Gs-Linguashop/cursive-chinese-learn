document.addEventListener("DOMContentLoaded", () => {

  const input = document.getElementById("charInput");
  const output = document.getElementById("output");
  const hint = document.getElementById("hint");

  let CHAR_MAP = {};

  // Load external JSON
  fetch("links.json")
    .then(res => res.json())
    .then(data => {
      CHAR_MAP = data;
      hint.textContent = "";
      console.log("Loaded CHAR_MAP:", CHAR_MAP);
    })
    .catch(err => {
      hint.textContent = "加载字典失败，请检查 links.json";
      console.error("Failed to load links.json:", err);
    });

  function renderSVG(path, char) {
    output.innerHTML = "";
    const img = document.createElement("img");
    img.src = path;
    img.alt = char;
    output.appendChild(img);
  }

  function search() {
    const c = input.value.trim();
    if (!c) {
      hint.textContent = "";
      output.innerHTML = "";
      return;
    }

    const path = CHAR_MAP[c];
    if (!path) {
      hint.textContent = "未找到该汉字";
      output.innerHTML = "";
      return;
    }

    hint.textContent = "";
    renderSVG(path, c);
  }

  // Automatic search whenever the input changes
  input.addEventListener("input", search);

});
