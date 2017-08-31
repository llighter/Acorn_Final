var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["ㄱ카페", "ㄴ카페", "ㄷ카페", "공상", "씨유", "지에스"],
        datasets: [{
            label: '아메리카노',
            data: [3000, 4500, 2000, 1500, 1000, 1500],
            
            backgroundColor: [
                'rgba(100, 99, 132, 0.2)','rgba(0, 99, 132, 0.2)','rgba(0, 50, 100, 0.2)','rgba(60, 250, 200, 0.2)','rgba(0, 0, 100, 0.2)','rgba(0, 0, 0, 0.2)'
            ],
            borderColor: [
                'rgba(100,99,132,1)','rgba(0, 99, 132, 1)','rgba(0, 50, 100, 1)','rgba(60, 250, 200, 1)','rgba(0, 0, 100, 1)','rgba(0, 0, 0, 1)'
            ],
            borderWidth: 1,
            borderWidth : '1',
            hoverBorderWidth : '3',


        },{

            label: '라떼',
            data: [4000, 5000, 3000, 2000, 1500, 1700],
            backgroundColor: [
                'rgba(100, 99, 132, 0.4)','rgba(0, 99, 132, 0.4)','rgba(0, 50, 100, 0.4)','rgba(60, 250, 200, 0.4)','rgba(0, 0, 100, 0.4)','rgba(0, 0, 0, 0.4)'
            ],
            borderColor: [
                'rgba(100,99,132,1)','rgba(0, 99, 132, 1)','rgba(0, 50, 100, 1)','rgba(60, 250, 200, 1)','rgba(0, 0, 100, 1)','rgba(0, 0, 0, 1)'
            ],
            borderWidth: 1,
            borderWidth : '2',
            hoverBorderWidth : '5',

        }]
    },
    options: {
        responsive: true,
        title:{
            display:true,
            text:'커피가격'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '카페'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '가격'
                },
                ticks: {
                    suggestedMin: 0, // 일반적인 최소값(강제적X) 작은값이 있으면 자동으로 변경
                    suggestedMax: 6000, // 일반적인 최대값(강제적X)
                    stepSize: 500 // 스탭사이즈
                }
            }]
        }





    },

});