/**
 * Theme: Minton Admin Template
 * Author: Coderthemes
 * Module/App: Flot-Chart
 */

! function($) {
	"use strict";

	var FlotChart = function() {
		this.$body = $("body")
		this.$realData = []
	};

	//creates Combine Chart
	FlotChart.prototype.createCombineGraph = function(selector, ticks, labels, datas) {
		var data = [{
			label : labels[0],
			data : datas[0],
			lines : {
				show : true
			}
		},
		{
			label : labels[1],
			data : datas[1],
			lines : {
				show : true
			}
		},
		{
			label : labels[2],
			data : datas[2],
			lines : {
				show : true
			}
		}];
		var options = {
			series : {
				shadowSize : 0
			},
			grid : {
				hoverable : true,
				clickable : true,
				tickColor : "#98a6ad",
				borderWidth : 1,
				borderColor : "#58666e"
			},
			colors : ["#3bafda", "#f76397", "#00b19d"],
			tooltip : true,
			tooltipOpts : {
				defaultTheme : false
			},
			legend : {
				position : "ne",
				margin : [0, -24],
				noColumns : 0,
				labelBoxBorderColor : null,
				labelFormatter : function(label, series) {
					// just add some space to labes
					return '' + label + '&nbsp;&nbsp;';
				},
				width : 30,
				height : 2
			},
			yaxis : {
				tickColor :  'rgba(0,0,0,0.1)', //'#98a6ad',
				font : {
					color : '#bdbdbd'
				}
			},
			xaxis : {
				ticks: ticks,
				tickColor : 'rgba(0,0,0,0.1)', //'#98a6ad',
				font : {
					color : '#bdbdbd'
				}
			}
		};

		$.plot($(selector), data, options);
	},

	//initializing various charts and components
	FlotChart.prototype.init = function() {

		//Combine graph data
		var Nasdaq = [[0.1, 201], [1.4, 520], [2, 337], [3, 261], [4, 157], [5, 95], [6, 200], [7, 250], [8, 320], [9, 500], [10, 152], [11, 214], [12, 364], [13, 449], [14, 558], [15, 282], [16, 379], [17, 429], [18, 518], [19, 470], [20, 330], [21, 245], [22, 358], [23, 74]];
		var DJIA = [[0, 311], [1, 630], [2, 447], [3, 371], [4, 267], [5, 205], [6, 310], [7, 360], [8, 430], [9, 610], [10, 262], [11, 324], [12, 474], [13, 559], [14, 668], [15, 392], [16, 489], [17, 539], [18, 628], [19, 580], [20, 440], [21, 355], [22, 468], [23, 184]];
		var SP500 = [[23, 727], [22, 128], [21, 110], [20, 92], [19, 172], [18, 63], [17, 150], [16, 592], [15, 12], [14, 246], [13, 52], [12, 149], [11, 123], [10, 2], [9, 325], [8, 10], [7, 15], [6, 89], [5, 65], [4, 77], [3, 600], [2, 200], [1, 385], [0, 200]];
		var ticks = [[0, "9:30am"], [1, ""], [2, "00h"], [3, ""], [4, "02h"], [5, ""], [6, "04h"], [7, ""], [8, "06h"], [9, ""], [10, "08h"], [11, ""], [12, "10h"], [13, ""], [14, "12h"], [15, ""], [16, "14h"], [17, ""], [18, "16h"], [19, ""], [20, "18h"], [21, ""], [22, "20h"], [23, ""]];
		var combinelabels = ["Nasdaq", "DJIA", "S&P 500"];
		var combinedatas = [Nasdaq, DJIA, SP500];

		this.createCombineGraph("#combine-chart #combine-chart-container", ticks, combinelabels, combinedatas);
	},

	//init flotchart
	$.FlotChart = new FlotChart, $.FlotChart.Constructor = FlotChart

}(window.jQuery),

//initializing flotchart
function($) {
	"use strict";
	$.FlotChart.init()
}(window.jQuery);

$(document).ready(function() {

});
