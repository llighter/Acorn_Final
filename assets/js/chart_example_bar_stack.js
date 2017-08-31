var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["1월", "2월", "3월", "4월", "5월", "6월"],
        datasets: [{
            label: '아메리카노',
            data: [3000, 4500, 2000, 1500, 1000, 1500],
            backgroundColor : 'rgba(100, 99, 132, 0.8)',
         
        },{
            label: '라떼',
            data: [3000, 4500, 2000, 1500, 1000, 1500],
            backgroundColor : 'rgba(0, 99, 132, 0.8)',
   
        }]
    },
    options: {
        responsive: true,
        tooltips: {
            mode: 'index',
            intersect: false
        },
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
            },
            stacked: true
        }],
        yAxes: [{
            display: true,
            scaleLabel: {
                display: true,
                labelString: '가격'
            },
            stacked: true,
            ticks: {
                suggestedMin: 0, // 일반적인 최소값(강제적X) 작은값이 있으면 자동으로 변경
                suggestedMax: 6000, // 일반적인 최대값(강제적X)
                stepSize: 500 // 스탭사이즈
            }
        }]
        }
    },

});