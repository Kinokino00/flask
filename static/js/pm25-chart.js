let chart1 = echarts.init(document.getElementById('main'));
let chart2 = echarts.init(document.getElementById('six-county'));
let chart3 = echarts.init(document.getElementById('county'));
// let chart4 = echarts.init(document.getElementById('county2'));
const selectCountyEl = document.querySelector("#selectCounty");
selectCountyEl.addEventListener("change", () => {
    drawCountyPM25(selectCountyEl.value);
})
drawPM25();
// chartPie(chart4, "Pie Chart", [
//     { value: 1048, name: 'Search Engine' },
//     { value: 735, name: 'Direct' },
//     { value: 580, name: 'Email' },
//     { value: 484, name: 'Union Ads' },
//     { value: 300, name: 'Video Ads' }
// ]);
// function chartPie(chart, title, data) {
//     let option = {
//         title: {
//             text: title,
//             left: 'center'
//         },
//         tooltip: {
//             trigger: 'item'
//         },
//         legend: {
//             orient: 'vertical',
//             left: 'left'
//         },
//         series: [
//             {
//                 name: 'Access From',
//                 type: 'pie',
//                 radius: '50%',
//                 data: data,
//                 emphasis: {
//                     itemStyle: {
//                         shadowBlur: 10,
//                         shadowOffsetX: 0,
//                         shadowColor: 'rgba(0, 0, 0, 0.5)'
//                     }
//                 }
//             }
//         ]
//     };
//     chart.setOption(option);
// }
function chartPic(chart, title, label, xData, yData, color = "#00008b") {
    let option = {
        title: {
            text: title
        },
        tooltip: {},
        legend: {
            data: label
        },
        xAxis: {
            data: xData
        },
        yAxis: {},
        series: [
            {
                itemStyle: {
                    color: color
                },
                name: label,
                type: 'bar',
                data: yData
            }
        ]
    };
    chart.setOption(option);
}
function drawCountyPM25(county) {
    chart3.showLoading();
    $.ajax(
        {
            url: '/county-pm25-json/' + county,
            type: 'GET',
            dataType: 'json',
            success: (result) => {
                chart3.hideLoading();
                if (!result['success']) {
                    county = county + "輸入不正確..."
                }
                chartPic(chart3, county, "PM2.5", Object.keys(result['pm25']), Object.values(result['pm25']), color = "#0088b4");
            },
            error: () => {
                chart3.showLoading();
                alert('取得資料失敗!')
            }
        }
    )
};
function drawPM25() {
    chart1.showLoading();
    chart2.showLoading();
    $.ajax(
        {
            url: '/pm25-json', //呼叫main.py寫的route路徑
            type: 'GET',
            dataType: 'json',
            success: (result) => { //此為main.py return的值
                chart1.hideLoading();
                chart2.hideLoading();
                chartPic(chart1, result['title'], "PM2.5", result['xData'], result['yData'], color = "#ff99b4");
                chartPic(chart2, "六都PM2.5平均值", "PM2.5", Object.keys(result['six_data']), Object.values(result['six_data']), color = "#ff69b4");
                drawCountyPM25(result['county']);
            },
            error: () => {
                chart1.hideLoading();
                chart2.hideLoading();
                alert('取得資料失敗!')
            }
        }
    )
};
window.onresize = function () {
    chart1.resize();
    chart2.resize();
    chart3.resize();
};