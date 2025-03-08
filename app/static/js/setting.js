// ユーザー名変更
const edit = document.getElementById("edit");
const save = document.getElementById("save");
const usernameDisplay = document.getElementById("usernameDisplay");
const usernameInput = document.getElementById("usernameInput");

edit.addEventListener("click", () => {
  usernameInput.value = usernameDisplay.textContent;
  usernameInput.style.display = "block";
  save.style.display = "block";
  usernameDisplay.style.display = "none";
  edit.style.display = "none";
});

usernameInput.addEventListener("input", () => {
  save.disabled = usernameInput.value.trim() === "";
});

save.addEventListener("click", async () => {
  const newUsername = usernameInput.value;

  try {
    const response = await fetch("/update-username", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: newUsername }),
    });

    if (response.ok) {
      usernameDisplay.textContent = newUsername;
      usernameDisplay.style.display = "block";
      usernameInput.style.display = "none";
      save.style.display = "none";
      edit.style.display = "block";
    } else {
      alert("更新に失敗しました");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("エラーが発生しました");
  }
});

// 観光地登録
// 地域を取得
document.addEventListener("DOMContentLoaded", async () => {
  const locationSelect = document.getElementById("location");
  const stationSelect = document.getElementById("station");

  // 地域を取得
  try {
    const response = await fetch("/get-regions");
    if (!response.ok) {
      throw new Error("Network response was not ok: " + response.statusText);
    }

    const regions = await response.json();

    regions.forEach((region) => {
      const option = document.createElement("option");
      option.value = region.region_id; // region_idをvalueに設定
      option.textContent = region.region_name; // region_nameを表示
      locationSelect.appendChild(option); // 地域のプルダウンに追加
    });
  } catch (error) {
    console.error("Error fetching regions:", error);
    alert("地域の取得に失敗しました");
  }

  // 地域選択時のイベント
  locationSelect.addEventListener("change", async function () {
    const regionId = this.value;

    if (regionId) {
      try {
        const response = await fetch(`/get-stations/${regionId}`);
        const stations = await response.json();

        stationSelect.innerHTML =
          '<option value="" selected disabled>気象台を選択してください</option>';

        stations.forEach((station) => {
          const option = document.createElement("option");
          option.value = station.station_id;
          option.textContent = station.station_name;
          stationSelect.appendChild(option);
        });
      } catch (error) {
        console.error("Error fetching stations:", error);
        alert("気象台の取得に失敗しました");
      }
    }
  });
});
