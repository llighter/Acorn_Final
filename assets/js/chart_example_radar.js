var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'radar',
    data: {
        labels: ["힘", "민첩", "지혜", "체력", "지능", "운"],
        datasets: [{
            label: '활쟁이',
            data: [15, 77, 32, 25, 21, 35],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
            ],
            borderColor: [
                'rgba(255,99,132,1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        legend: {
            position: 'bottom',
        },
        responsive: true,
        title:{
            display:true,
            text:'스텟'
        },
        scale: {
          ticks: {
            beginAtZero: true
          }
        }
    }
});