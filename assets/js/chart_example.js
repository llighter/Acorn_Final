var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["8/10", "8/11", "8/12", "8/13", "8/14", "8/15"],
        datasets: [{
            label: 'price of iPhone7',
            data: [12, 19, 3, 5, 2, 3],
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
        responsive: true,
        title:{
            display:true,
            text:'iPhone7'
        },
        scales: {
            xAxes: [{
                display: true,
            }],
            yAxes: [{
                display: true,
                // type: 'logarithmic',
            }]
        },
        annotation: {
            events: ['click'],
            annotations: [{
                drawTime: 'afterDraw',
                id: 'hline',
                type: 'line',
                mode: 'horizontal',
                scaleID: 'y-axis-0',
                value: 7,
                borderColor: 'red',
                borderWidth: 2,
                label: {
                    backgroundColor: "red",
                    content: "Mean",
                    enabled: true
                }
            }, {
                drawTime: 'afterDraw',
                id: 'vline',
                type: 'line',
                mode: 'vertical',
                scaleID: 'x-axis-0',
                value: '8/12',
                borderColor: 'orange',
                borderWidth: 2,
                label: {
                    backgroundColor: "red",
                    content: "Release Day",
                    enabled: true
                }
            }]
        }
    }
});