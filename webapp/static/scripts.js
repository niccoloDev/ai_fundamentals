<!-- handle radio button change selection -->
$(document).ready(function(){
    $('.gen_strategy_class').change(function(){
        // code to be executed when the radio button changes value
        const selectedValue = $(this).val();
        if( selectedValue === "Choose" ) {
            $('.tickers').show();
            $('.tickers_num').hide().val("");

        }
        else if( selectedValue === "Random" ) {
            $('.tickers').hide().val("");
            $('.tickers_num').show();
        }
    })
});

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}


<!-- handle pie graph and progress bar (websocket communication) -->
document.addEventListener('DOMContentLoaded', (event) => {
            const socket = io.connect('http://' + document.domain + ':' + location.port + '/portfolio_generation');

            socket.on('connect', function() {
                console.log('Connected');

            });

            socket.on('progress_update', function(msg) {
                //console.log(msg.progress)
                const progressBar = document.getElementById('algoProgressBar');
                progressBar.style.width = msg.progress + '%';
                progressBar.setAttribute('aria-valuenow', msg.progress);
            });

            let pieChart = null
            socket.on('server_response', function(msg) {
                console.log('Current best portfolio: ' + JSON.stringify(msg.current_best_portfolio));
                const json_response = JSON.stringify(msg.current_best_portfolio)
                //const json_response = '{"assets":[{"ticker":"FUND","weight":0},{"ticker":"ACACU","weight":0.3898056901949911},{"ticker":"FCAP","weight":0},{"ticker":"LANC","weight":0.6664117870354779},{"ticker":"DRTS","weight":0.001035460834053781}],"fitness":2.049605048795377}'
                const portfolio = JSON.parse(json_response);
                var xValues = portfolio.assets.map(p => p.ticker+': '+((p.weight * 100).toFixed(2))+'%');
                var yValues = portfolio.assets.map(p => p.weight);
                var barColors = portfolio.assets.map(_ => getRandomColor());


                if (pieChart !== null) {
                    pieChart.destroy();
                }

                pieChart = new Chart("pieChart", {
                  type: "pie",
                  data: {
                    labels: xValues,
                    datasets: [{
                      backgroundColor: barColors,
                      data: yValues
                    }]
                  },
                  options: {
                    title: {
                      position: 'top',
                      fontColor: 'white',
                      fontSize: 18,
                      display: true,
                      text: "Fitness: " + portfolio.fitness.toFixed(2)
                    },
                    legend: {
                        position: 'left',
                        labels: {
                            // This more specific font property overrides the global property
                            fontColor: 'white',
                            fontSize: 14
                        }
                    }
                  }
                });
            });
        });

