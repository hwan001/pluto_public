function draw_graph(arr_data, tickers_len, tickers){
    for (var i=0; i < tickers_len; i++){
        var chart = new Chart(document.getElementById("TSLA").getContext('2d'), {
        type: 'line',
        data: {
            labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            datasets: [{
            label: "Closing price",
            backgroundColor: 'transparent',
            borderColor: 'aliceblue',
            data: arr_data[i],
            }]
        },
        options: {
            scales: {
	    		yAxes: [{
	    			ticks: {
	    				stepSize : 1,
	    				fontSize : 12,
	    			}
	    		}]
	    	}
        }
        });
    }
}