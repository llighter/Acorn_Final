var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["12/3", "12/6", "12/9", "12/12", "13/3", "13/6","13/9","13/12","14/3","14/6","14/9","14/12"],
        datasets: [{
            type: 'line',
            label : '아이폰4s',
            lineTension : ['0.1'], // 라인 곡선
            data: [420000, 390000, 380000, 370000, 330000, 315000, 310000, 250000, 240000, 210000, 200000, 210000],
            backgroundColor: 'rgba(238, 194, 100, 0.2)', // 칠해지는 영역색
            borderColor: 'rgba(238, 194, 100, 0.7)', // 선색
            pointStyle : '',
            pointBorderColor : 'rgba(238, 194, 100, 1)', // 포인트 외각선 색
            pointHoverBackgroundColor : 'rgba(238, 194, 100, 1)', // 호버시 포인트 색
            pointRadius : '3', // 평소 포인트 사이즈
            pointHoverRadius : '5', // 호버시 포인트 사이즈
            fill: 'start', // 채우기 옵션
        }]
    },
    options: {
        responsive: true,
        legend: {
            position : 'bottom', // 라벨 위치
        },
        title:{
            display:true,
            text:'아이폰 평균가격'
        },
        tooltips: { // 수치값 한번에 보기
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '기간'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '평균가격'
                },
                ticks: {
                    suggestedMin: 250000, // 일반적인 최소값(강제적X) 작은값이 있으면 자동으로 변경
                    suggestedMax: 500000, // 일반적인 최대값(강제적X)
                    stepSize: 30000 // 스탭사이즈
                }

            }]
        },
        annotation: {
            
            annotations: [{ // 중앙 포인트선
                drawTime: 'afterDraw',
                id: 'hline',
                type: 'line',
                mode: 'horizontal',
                scaleID: 'y-axis-0',
                value: 450000,
                borderColor: 'red',
                borderWidth: 2,
                label: {
                    backgroundColor: "red",
                    content: "임의의평균가",
                    enabled: true
                }
            }, {
                drawTime: 'afterDraw',
                id: 'vline',
                type: 'line',
                mode: 'vertical',
                scaleID: 'x-axis-0',
                value: '13/9',
                borderColor: 'orange',
                borderWidth: 2,
                label: {
                    backgroundColor: "red",
                    content: "아이폰5c출시",
                    enabled: true
                }
            }]
        }
        
    }


});