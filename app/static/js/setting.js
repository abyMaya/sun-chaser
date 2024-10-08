// ユーザー名変更
const edit = document.getElementById('edit');
const save = document.getElementById('save');
const usernameDisplay = document.getElementById('usernameDisplay');
const usernameInput = document.getElementById('usernameInput');

edit.addEventListener('click', () => {
  usernameInput.value = usernameDisplay.textContent;
  usernameInput.style.display = 'block';
  save.style.display = 'block';
  usernameDisplay.style.display = 'none';
  edit.style.display = 'none';
});

usernameInput.addEventListener('input', () => {
  save.disabled = usernameInput.value.trim() === '';
});

save.addEventListener('click', async () => {
  const newUsername = usernameInput.value;

  try {
    const response = await fetch('/update-username', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: newUsername}),
    });

    if (response.ok) {
        usernameDisplay.textContent = newUsername;
        usernameDisplay.style.display = 'block';
        usernameInput.style.display = 'none';
        save.style.display = 'none';
        edit.style.display = 'block';
    } else {
        alert('更新に失敗しました');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('エラーが発生しました');
  }
});

// 観光地登録
// 地域を取得
document.addEventListener("DOMContentLoaded", async () => {
  const locationSelect = document.getElementById('location');
  const selectedStationDisplay = document.getElementById('selectedStationName');  // 表示用の変数名変更

  // 地域を取得
  try {
      const response = await fetch('/get-regions');
      if (!response.ok) {
          throw new Error('Network response was not ok: ' + response.statusText);
      }

      const regions = await response.json();

      regions.forEach(region => {
          const option = document.createElement('option');
          option.value = region.region_id;  // region_idをvalueに設定
          option.textContent = region.region_name;  // region_nameを表示
          locationSelect.appendChild(option); // 地域のプルダウンに追加
      });
  } catch (error) {
      console.error('Error fetching regions:', error);
      alert('地域の取得に失敗しました');
  }

  // 地域選択時のイベント
  locationSelect.addEventListener('change', async function() {
    const regionId = this.value;

    if (regionId) {
        try {
            const response = await fetch(`/get-stations/${regionId}`);
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }

            const stations = await response.json();

            // プルダウンメニューをクリアし、気象台の選択肢を追加
            this.innerHTML = `<option value="" selected disabled>気象台を選択してください</option>`;
            
            stations.forEach(station => {
                const option = document.createElement('option');
                option.value = station.station_id; 
                option.textContent = station.station_name; 
                this.appendChild(option);
            });

        } catch (error) {
            console.error('Error fetching stations:', error);
            alert('気象台の取得に失敗しました');
        }
    }
  });

  // 気象台選択時のイベント
  locationSelect.addEventListener('change', function() {
    const selectedStationId = this.value; // 選択された気象台のIDを取得
    const selectedStationName = this.options[this.selectedIndex].text; // 選択された気象台名を取得

    // 選択された気象台名を表示用の要素に反映
    selectedStationDisplay.textContent = `選択された気象台: ${selectedStationName}`;
  });
});