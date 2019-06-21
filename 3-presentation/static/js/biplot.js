
function get_viz_size() {
  graphHeight = document.getElementById('viz').clientHeight;
  graphWidth = document.getElementById('viz').clientWidth;
  return {
    h: graphHeight,
    w: graphWidth,
    xmid: graphWidth/2,
    ymid: graphHeight/2
  }
}

function initialize_tooltip() {
  // Define the div for the tooltip
  var tooltip = d3.select("#viz").append("div") 
      .attr("class", "tooltip")       
      .attr("id", "tooltip")       
      .style("opacity", 0);
}

function tooltip_on(d) {    
  div = d3.select("#tooltip")

  var variable = get_variable()
  var format = get_format(variable)


  // could possibly use absolute position if this wasn't attached to a div?
  viz_top = document.getElementById('viz').getBoundingClientRect().top
  viz_left = document.getElementById('viz').getBoundingClientRect().left


  div.transition()    
      .duration(200)    
      .style("opacity", .9);    
  div.html("<b>" + d["dept"] + "</b><br>" + format(d[variable]))  
      .style("left", (d3.event.pageX-viz_left) + "px")   
      .style("top", (d3.event.pageY-viz_top-28) + "px"); 

};

function tooltip_off(d) {   
  div = d3.select("#tooltip")
  div.transition()    
      .duration(500)    
      .style("opacity", 0); 
  update_barchart(data)
};

function initialize_visualization(data) {

  initialize_tooltip()
  
  var div_size = get_viz_size()

  // get default values
  var x_variable = document.getElementById("x_dropdown").value
  var y_variable = document.getElementById("y_dropdown").value

  // set labels
  var x_variable_axis_label = x_variable
  var y_variable_axis_label = y_variable


  // setting formating for chart
  var margin = {top: 50, right: 50, bottom: 50, left: 50},
      width = div_size.w - margin.left - margin.right,
      height = div_size.h - margin.top - margin.bottom;


  // create our svg
  var svg = d3.select("#viz").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("id","viz_svg")
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


  // setting scale based on formating
  var xScale = d3.scalePow().exponent(.5).range([0, width]);
  var yScale = d3.scalePow().exponent(.5).range([height, 0]);


  //create the axes
  var formatPercent = d3.format(".0%");
  var xAxis = d3.axisBottom().scale(xScale)
  var yAxis = d3.axisLeft().scale(yScale)



  // now let's run on top of the data!

  // each object when read is initially a string, this makes everything a number
  data.forEach(function(d) {
    d[x_variable] = +d[x_variable];
    d[y_variable] = +d[y_variable];
  });

  // this presets the low and high end to reflect the data
  xScale.domain(d3.extent(data, function(d) { return d[x_variable]; })).nice();
  yScale.domain(d3.extent(data, function(d) { return d[y_variable]; })).nice();

  // x axis & labeling
  // creating a svg group
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)

  // y axis & labeling
  // creating a svg group
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)

  // text label for the y axis
  svg.append("text")
      .attr("class", "y axis label")
      .attr("transform", "rotate(-90)")
      .attr("font-family", "Archivo Narrow")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text(y_variable_axis_label);    


  // text label for the x axis
  svg.append("text")             
      .attr("class", "x axis label")
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.top - 10) + ")")
      .attr("font-family", "Archivo Narrow")
      .style("text-anchor", "middle")
      .text(x_variable_axis_label)
      .style("color", "black")

  // place dots
  svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", function(d) { return 5 })
      .attr("cx", function(d) { return xScale(d[x_variable]); })
      .attr("cy", function(d) { return yScale(d[y_variable]); })
      .style("fill", function(d) { return "blue" })
      .attr("opacity",.5)
      .on("mouseover", function(d) { tooltip_on(d) })
      .on("mouseout", function(d) { tooltip_off(d) })


}


function updateBiplot(data) {

  var div_size = get_viz_size()

  var svg = d3.select("#viz_svg")

  // setting formating for chart
  var margin = {top: 50, right: 50, bottom: 50, left: 50},
      width = div_size.w - margin.left - margin.right,
      height = div_size.h - margin.top - margin.bottom;

  // get default values
  var x_variable = document.getElementById("x_dropdown").value
  var y_variable = document.getElementById("y_dropdown").value

  // set labels
  var x_variable_axis_label = x_variable
  var y_variable_axis_label = y_variable

  // setting scale based on formating
  var xScale = d3.scalePow().exponent(.5).range([0, width]);
  var yScale = d3.scalePow().exponent(.5).range([height, 0]);

  var xAxis = d3.axisBottom().scale(xScale)
  var yAxis = d3.axisLeft().scale(yScale)


  // each object when read is initially a string, this makes everything a number
  data.forEach(function(d) {
    d[x_variable] = +d[x_variable];
    d[y_variable] = +d[y_variable];
  });

  // this presets the low and high end to reflect the data
  xScale.domain(d3.extent(data, function(d) { return d[x_variable]; })).nice();
  yScale.domain(d3.extent(data, function(d) { return d[y_variable]; })).nice();


  // update dots
  svg.selectAll(".dot")
      .transition()
      .duration(2000)
      .attr("cx", function(d) { return xScale(d[x_variable]); })
      .attr("cy", function(d) { return yScale(d[y_variable]); })


  // update labels
  document.getElementsByClassName('x axis label')[0].innerHTML = x_variable_axis_label
  document.getElementsByClassName('y axis label')[0].innerHTML = y_variable_axis_label

  // update the x axis
  svg.select(".x")
      .transition()
      .duration(2000)
      .call(xAxis)

  // update the y axis
  svg.select(".y")
      .transition()
      .duration(2000)
      .call(yAxis)
}


