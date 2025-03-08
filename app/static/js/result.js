// URL パラメータから年月を取得する関数
function getMonthAndYearFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  const year = urlParams.get("year");
  const month = urlParams.get("month");
  const spotId = urlParams.get("spot_id");

  return { year, month, spotId };
}

// sunny_rateを取得する関数
export async function fetchSunnyRate(spotId, month) {
  try {
    const response = await fetch(
      `/get_sunny_rate?spot_id=${spotId}&month=${month}`,
    );
    if (!response.ok) {
      throw new Error("Failed to fetch sunny rate data");
    }

    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Error fetching sunny rate data:", error);

    return [];
  }
}

// 取得した年月を元にカレンダーを生成
function generateCalendar(year, month, sunnyRateData) {
  const calendarEl = document.getElementById("calendar2");
  const daysInMonth = new Date(year, month, 0).getDate(); // monthは1から12のためそのまま

  // 月を表す名前を取得
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const monthName = monthNames[month - 1];

  // 年月を表示するHTMLを追加
  let calendarHtml = `<h3 class="calendar-title">${year} ${monthName}</h3>`; // 年月を表示

  // カレンダーのHTML構造を生成
  calendarHtml += "<table><thead><tr>";
  for (let i = 0; i < 7; i++) {
    calendarHtml += `<th>${["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][i]}</th>`;
  }
  calendarHtml += "</tr></thead><tbody><tr>";

  // カレンダーの日付生成
  for (let i = 1; i <= daysInMonth; i++) {
    const dayOfWeek = new Date(year, month - 1, i).getDay(); // month-1で0から11の範囲に

    if (i === 1) {
      calendarHtml += "<tr>";
      for (let j = 0; j < dayOfWeek; j++) {
        calendarHtml += "<td></td>";
      }
    }

    // 晴れ率データを探して対応するアイコンを表示
    const sunnyRate =
      sunnyRateData?.find((item) => parseInt(item.day) === i)?.sunny_rate ||
      null;

    let icon = "";
    if (sunnyRate !== null) {
      if (sunnyRate >= 80) {
        icon = '<img src="../static/img/sun_high_2.png" alt="High Sunny Rate">';
      } else if (sunnyRate >= 65) {
        icon =
          '<img src="../static/img/sun_mid_2.png" alt="Medium Sunny Rate">';
      } else if (sunnyRate >= 50) {
        icon = '<img src="../static/img/sun_low_2.png" alt="Low Sunny Rate">';
      }
    }

    calendarHtml += `<td><span>${i}</span>${icon || ""}</td>`;

    if (dayOfWeek === 6) {
      calendarHtml += "</tr>";
      if (i < daysInMonth) {
        calendarHtml += "<tr>";
      }
    } else if (i === daysInMonth) {
      for (let j = dayOfWeek + 1; j <= 6; j++) {
        calendarHtml += "<td></td>";
      }
      calendarHtml += "</tr>";
    }
  }

  calendarHtml += "</tbody></table>";
  calendarEl.innerHTML = calendarHtml;
}

// ページがロードされた時にカレンダーを表示
try {
  document.addEventListener("DOMContentLoaded", async () => {
    const { year, month, spotId } = getMonthAndYearFromUrl();

    if (year && month && spotId) {
      try {
        const sunnyRateData = await fetchSunnyRate(spotId, `${year}-${month}`);
        generateCalendar(year, parseInt(month), sunnyRateData);
      } catch (error) {
        console.error("Error loading sunny rate data:", error);
      }
    } else {
      console.error("年月が指定されていません");
    }
  });
} catch (globalError) {
  console.error("Unhandled error in script:", globalError);
}
