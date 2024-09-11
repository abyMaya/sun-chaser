document.getElementById('serch-button').addEventListener('click', function(event) {
  event.preventDefault();  // デフォルトの動作を停止

  // フォームから年月の値を取得
  const monthInput = document.getElementById('month').value;

  // 必要な値が選択されているか確認
  if (monthInput) {
    // yearとmonthを分割してクエリパラメータに渡す
    const [year, month] = monthInput.split('-');
    const url = `result.html?year=${year}&month=${month}`;
    window.location.href = url;
  } else {
      alert("Please select a month.");
  }
});

