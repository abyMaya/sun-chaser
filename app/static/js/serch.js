document.getElementById('serch-button').addEventListener('click', async function(event) {
  event.preventDefault();  // デフォルトの動作を停止

  // スポット年月の値を取得
  const spotInput = document.getElementById('spotsSelect').value;
  const monthInput = document.getElementById('month').value;

  // 必要な値が選択されているか確認
  if (spotInput && monthInput) {
    const [year, month] = monthInput.split('-');

    try {
      // spot_idからstation_idを取得するためのリクエスト
      const response = await fetch(`/get_station_id?spot_id=${spotInput}`);
      
      // エラーチェック
      if (!response.ok) {
        const errorText = await response.text(); // レスポンスのテキストを取得
        console.error('Error fetching station_id:', errorText);
        throw new Error('Invalid spot_id');
      }

      const data = await response.json();
      const station_id = data.station_id;

      // デバッグログを追加
      console.log('Retrieved station_id:', station_id);

      // station_idを使って結果ページに遷移
      const url = `/result?spot_id=${spotInput}&station_id=${station_id}&year=${year}&month=${month}`;
      window.location.href = url;

    } catch (error) {
      console.error('Error:', error);
      alert('エラーが発生しました: ' + error.message);
    }
  } else {
    alert("観光地と月を選択してください");
  }
});

// 観光地を取得
document.addEventListener("DOMContentLoaded", async () => {
  const spotsSelect = document.getElementById('spotsSelect');
  
  
  // 観光地を取得
  try {
      const response = await fetch('/get-spots');
      if (!response.ok) {
          throw new Error('Network response was not ok: ' + response.statusText);
      }

      const spots = await response.json();

      spots.forEach(spot=> {
          const option = document.createElement('option');
          option.value = spot.spot_id;  
          option.textContent = spot.spot_name;  

          spotsSelect.appendChild(option); 
      });
  } catch (error) {
      console.error('Error fetching regions:', error);
      alert('観光地の取得に失敗しました');
  }
});
