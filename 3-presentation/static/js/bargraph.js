
var value_labels = false
var bar_labels = false

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


function hide_dropdown2(){
  dropdown = d3.select("#dropdown2")
  dropdown.transition()    
      .duration(500)    
      .style("opacity", 0); 
}

function unhide_dropdown2(){
  dropdown = d3.select("#dropdown2")
  dropdown.transition()    
      .duration(500)    
      .style("opacity", 1); 
}

function get_variable(){
  var v1 = document.getElementById("dropdown1").value
  return v1
}

function get_format(variable){
  if (variable.includes("%")){
    return d3.format(".1%");
  }
  if (variable.includes("tag")){
    return d3.format(".1%");
  }
  if (variable.includes("$")){
    return d3.format("$,.0d");
  }
  if (variable.includes("#")){
    return d3.format(",.0d");
  }
  else {
    return d3.format(",.2f")
  }
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


function initialize_barchart(data) {

  initialize_tooltip()
  
  var div_size = get_viz_size()

  // get default values
  var variable = get_variable()

  // convert all values to numbers (just to be sure)
  data.forEach(function(d) {
    d[variable] = +d[variable]  
  })

  // sort by the selected variable
  data = data.sort(function(a, b){
     return d3.ascending(a[variable], b[variable]);
  })

  // create rank property
  for (var i = 0; i < data.length; i++) {
    data[i].rank = i + 1;
  }

  // set labels
  var y_variable_axis_label = "Dept"
  var x_variable_axis_label = variable

  // setting formating for chart
  var margin = {top: 50, right: 50, bottom: 100, left: 50},
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
  var xScale = d3.scaleLinear().range([0, width]);
  var yScale = d3.scaleLinear().range([height, 0]);

  //create the axes
  var format = get_format(variable)
  var xAxis = d3.axisBottom().scale(xScale)
  var yAxis = d3.axisLeft().scale(yScale)

  // now let's run on top of the data!

  // each object when read is initially a string, this makes everything a number
  data.forEach(function(d) {
    d[variable] = +d[variable];
  });

  // this presets the low and high end to reflect the data
  yScale.domain([0,data.length]);
  xScale.domain(d3.extent(data, function(d) { return d[variable]*1.1; })).nice();

  // x axis & labeling
  // creating a svg group
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(40," + height + ")")
      .call(xAxis.tickFormat(format))

  // // y axis & labeling
  // // creating a svg group
  // svg.append("g")
  //     .attr("class", "y axis")
  //     .call(yAxis)

  // text label for the y axis
  svg.append("text")
      .attr("class", "y_axis_label")
      .attr("transform", "rotate(-90)")
      .attr("font-family", "Archivo Narrow")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text(y_variable_axis_label);    


  // text label for the x axis
  svg.append("text")             
      .attr("class", "x_axis_label")
      .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + margin.bottom - 10) + ")")
      .attr("font-family", "Archivo Narrow")
      .style("text-anchor", "middle")
      .text(x_variable_axis_label)
      .style("color", "black")

  // place bars
  svg.selectAll(".bar")
      .data(data)
    .enter().append("a")
      .attr("xlink:href", function(d) { return "/scorecard?subject="+d['dept'] })
    .append("rect")
      .attr("class", "bar")
      .attr("height", height/data.length*.9 )
      .attr("width", function(d) { return xScale(d[variable]); })
      .attr("y", function(d,i) { return yScale(d.rank); })
      .attr("x", "40")
      .style("fill", function(d) { return "blue" })
      .attr("opacity",.5)
      .on("mouseover", function(d) {
          d3.select(this).transition().duration(500).attr("opacity",1);
          tooltip_on(d);
        })
      .on("mouseout", function(d) {
          d3.select(this).transition().duration(500).attr("opacity",.5);
          tooltip_off(d);
        })

  if (bar_labels == true) {

    // place labels
    svg.selectAll(".barLabel")
        .data(data)
      .enter().append("text")
        .attr("class", "valueLabel")
        .attr("x", 0)
        .attr("y", function(d,i) { return yScale(d.rank) + height/data.length/2; })
        .attr('text-anchor','start')
        .attr('font-size',"20px")
        .text(function(d,i) { return d['dept']; })

      }


  if (value_labels == true) {

    // place labels
    svg.selectAll(".valueLabel")
        .data(data)
      .enter().append("text")
        .attr("class", "valueLabel")
        .attr("x", function(d) { return xScale(d[variable]) + 50; })
        .attr("y", function(d,i) { return yScale(d.rank) + height/data.length/2; })
        .attr('text-anchor','start')
        .text(function(d,i) { return format(d[variable]); })

      }

  // place images
  // svg.selectAll(".img")
  //       .data(data)
  //     .enter().append("svg:image")
  //     .attr("class", "img")
  //     .attr("xlink:href", function(d) { return d['image']})
  //     .attr("x", "0")
  //     .attr("y", function(d,i) { return yScale(d.rank); })
  //     .attr("height", height/data.length*.9 )
}


function update_barchart(data) {

  var div_size = get_viz_size()

  var svg = d3.select("#viz_svg")

  // setting formating for chart
  var margin = {top: 50, right: 50, bottom: 100, left: 50},
      width = div_size.w - margin.left - margin.right,
      height = div_size.h - margin.top - margin.bottom;

  // get default values
  var variable = get_variable()


  // set labels
  var x_variable_axis_label = variable
  var y_variable_axis_label = "Dept"

  // setting scale based on formating
  var xScale = d3.scaleLinear().range([0, width]);
  var yScale = d3.scaleLinear().range([height, 0]);

  //create the axes
  //create the axes
  var format = get_format(variable)
  var xAxis = d3.axisBottom().scale(xScale)
  var yAxis = d3.axisLeft().scale(yScale)

  // now let's run on top of the data!

  // each object when read is initially a string, this makes everything a number
  data.forEach(function(d) {
    d[variable] = +d[variable];
  });

  // sort by the selected variable
  data = data.sort(function(a, b){
     return d3.ascending(a[variable], b[variable]);
  })

  // update rank
  for (var i = 0; i < data.length; i++) {
    data[i].rank = i + 1;
  }

  // this presets the low and high end to reflect the data
  yScale.domain([0,data.length]);
  xScale.domain(d3.extent(data, function(d) { return d[variable]*1.1; })).nice();

  // update bars
  svg.selectAll(".bar")
      .transition()
      .duration(1000)
      .attr("class", "bar")
      .attr("height", height/data.length*.9 )
      .attr("width", function(d) { return xScale(d[variable]); })
      .attr("y", function(d,i) { return yScale(d.rank); })
      .attr("opacity",.5)


  // update images
  svg.selectAll(".img")
      .transition()
      .duration(1000)
      .attr("class", "img")
      .attr("height", height/data.length*.9 )
      .attr("y", function(d,i) { return yScale(d.rank); })

  // place value labels

  if (value_labels == true) {
    svg.selectAll(".valueLabel")
        .transition()
        .duration(1000)
        .attr("class", "valueLabel")
        .attr("x", function(d) { return xScale(d[variable]) + 50; })
        .attr("y", function(d,i) { return yScale(d.rank) + height/data.length/2; })
        .text(function(d,i) { return format(d[variable]); })
  }

  // update labels
  document.getElementsByClassName('x_axis_label')[0].innerHTML = x_variable_axis_label
  document.getElementsByClassName('y_axis_label')[0].innerHTML = y_variable_axis_label

  // update the x axis
  svg.select(".x")
      .transition()
      .duration(2000)
      .call(xAxis.tickFormat(format))

  // // update the y axis
  // svg.select(".y")
  //     .transition()
  //     .duration(2000)
  //     .call(yAxis)
}


