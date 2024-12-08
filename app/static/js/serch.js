import { fetchSunnyRate } from './result.js';

document.addEventListener("DOMContentLoaded", async () => {
  // 観光地を取得する処理
  const spotsSelect = document.getElementById('spotsSelect');

  if (!spotsSelect) {
    console.error('Spots dropdown not found');
    return;
  }

  try {
    const response = await fetch('/get-spots');
    if (!response.ok) {
      throw new Error('Failed to fetch spots: ' + response.statusText);
    }

    const spots = await response.json();
    spots.forEach(spot => {
      const option = document.createElement('option');
      option.value = spot.spot_id;
      option.textContent = spot.spot_name;
      spotsSelect.appendChild(option);
    });

  } catch (error) {
    console.error('Error fetching spots:', error);
    alert('観光地の取得に失敗しました');
  }

  // 検索ボタンの処理
  const searchButton = document.getElementById('serch-button');
  
  if (!searchButton) {
    console.error('Search button not found');
    return;
  }

  searchButton.addEventListener('click', async function(event) {
    event.preventDefault(); // デフォルトの動作を停止

    // スポットと年月の値を取得
    const spotInput = document.getElementById('spotsSelect').value;
    const monthInput = document.getElementById('month').value;

    // 必要な値が選択されているか確認
    if (spotInput && monthInput) {
      const [year, month] = monthInput.split('-');

      try {
        // spot_idからstation_idを取得するリクエスト
        const response = await fetch(`/get_station_id?spot_id=${spotInput}`);
        if (!response.ok) {
          const errorText = await response.text();
          console.error('Error fetching station_id:', errorText);
          throw new Error('Invalid spot_id');
        }

        const data = await response.json();
        const station_id = data.station_id;

        // `fetchSunnyRate` を呼び出して天気データを取得
        const sunnyRateData = await fetchSunnyRate(station_id, `${year}-${month}`);
        console.log('Sunny rate data:', sunnyRateData);

        // station_idを使って結果ページに遷移
        const url = `/result?spot_id=${spotInput}&station_id=${station_id}&year=${year}&month=${month}`;
        window.location.href = url;
      } catch (error) {
        console.error('Error during search:', error);
        alert('エラーが発生しました: ' + error.message);
      }
    } else {
      alert("観光地と月を選択してください");
    }
  });
});
