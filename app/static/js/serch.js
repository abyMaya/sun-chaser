

document.getElementById('serch-button').addEventListener('click', function(event) {
  event.preventDefault();  // デフォルトの動作を停止

  // スポット年月の値を取得
  const spotInput = document.getElementById('spotsSelect').value;
  const monthInput = document.getElementById('month').value;

  // 必要な値が選択されているか確認
  if (spotInput && monthInput) {
    // yearとmonthを分割してクエリパラメータに渡す
    const [year, month] = monthInput.split('-');

    
    const url = `/result?spot=${spotInput}&year=${year}&month=${month}`;

    // 結果ページに遷移
    window.location.href = url;

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
