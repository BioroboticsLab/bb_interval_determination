var createTooltip = function(id, time_start, time_end, duration, filename_start, filename_end, info){
  var tooltip ="<table style=\"font-size:10px\">\
    <tr>\
        <td><b>Index:</b></td><td>{index}</td>\
    </tr>\
    <tr>\
        <td><b>Start:</b></td> <td>{time_start}</td>\
    </tr>\
     <tr>\
        <td><b>End:</b></td> <td>{time_end}</td>\
    </tr>\
    <tr>\
        <td><b>Duration:</b></td><td>{duration}</td>\
    </tr>\
    <tr>\
        <td><b>Filename Start:</b></td><td>{filename_start}</td>\
    </tr>\
    <tr>\
        <td><b>Filename End:</b></td><td>{filename_end}</td>\
    </tr>\
    <tr>\
        <td><b>Info:</b></td><td>{info}</td>\
    </tr>\
</table>"
  .replace("{index}", id)
  .replace("{time_start}", time_start)
  .replace("{time_end}", time_end)
  .replace("{duration}", duration)
  .replace("{filename_start}", filename_start)
  .replace("{filename_end}", filename_end)
  .replace("{info}", info)
return tooltip
}

var createTooltipSharedInterval = function(id, item){
  var duration = new Date(item["left"]["ts_end"]) - new Date(item["left"]["ts_start"]);
  if (item["left"] !== null)
    left = createTooltip(item["id"], item["left"]["ts_start"],item["left"]["ts_end"],
                         duration,item["left"]["start_video_name"],item["left"]["end_video_name"],item["left"]["info"])
  else
    left = 'nothing to see here..'
  if (item["right"] !== null)
    right = createTooltip(item["id"], item["right"]["ts_start"],item["right"]["ts_end"],
                         duration,item["right"]["start_video_name"],item["right"]["end_video_name"],item["right"]["info"])
  else
    right = 'nothing to see here..'
 var tooltip ="<table style=\"font-size:10px\">\
   <tr>\
       <th>Left</th><th>Right</th>\
   </tr>\
   <tr>\
       <td>{left}</td> <td>{right}</td>\
   </tr>\
</table>"
  .replace("{left}", left)
  .replace("{right}", right)
  return tooltip
}

var createSafeInterval = function(item, id, group){
  var new_item = {}
  var start = item["start_video_name"].split('--')[0].split('_')[2]
  var end = item["end_video_name"].split('--')[1].slice(0, 27)
  var duration = new Date(end) - new Date(start)
  new_item["id"] = id
  new_item["group"] = group
  new_item["start"] = start
  new_item["end"] = end
  new_item["content"] = item["id"].toString()
  new_item["title"] = createTooltip(item["id"].toString(), start, end, duration.toString(), item["start_video_name"], item["end_video_name"], item["info"])
  if (! item["stable"]){
    new_item["className"] = "unstable-interval";
  } else if (item["info"] === "ecc possible movement") {
    new_item["className"] = "possible-unstable-interval";
  } else {
    new_item["className"] = "stable-interval";
  }
  return new_item
}

var createTimeInterval = function(item, id, group){
  var new_item = {}
  var start = item["start_video_name"].split('--')[0].split('_')[2]
  var end = item["end_video_name"].split('--')[1].slice(0, 27)
  var duration = new Date(end) - new Date(start)
  new_item["id"] = id
  new_item["group"] = group
  new_item["start"] = start
  new_item["end"] = end
  new_item["content"] = item["id"].toString()
  new_item["title"] = createTooltip(item["id"].toString(), start, end, duration.toString(), item["start_video_name"], item["end_video_name"])
  if (item["id"] %2 === 0) {
    new_item["className"] = "even-interval";
  } else {
    new_item["className"] = "odd-interval";
  }
  return new_item
}

var createIntervalPair = function(item, id, group){
  console.log(item)
  var new_item = {}
  var start = item["ts_start"]
  var end = item["ts_end"]
  new_item["id"] = id
  new_item["start"] = start
  new_item["end"] = end
  new_item["group"] = group
  new_item["className"] = 'stable-interval';
  if (! item["stable"]){
    new_item["className"] = 'unstable-interval';
  }
  new_item["content"] = item['id'].toString();
  new_item["title"] = createTooltipSharedInterval(id, item)
  // new_item["title"] = createTooltip("", start, end, "1", item["left"]["start_video_name"], item["left"]["end_video_name"]);
  return new_item
}

var createOneSideFromIntervalPair = function(item, id, group, side){
  console.log(item)
  var new_item = {}
  if (item[side] === null)
    return null
  var start = item[side]["ts_start"]
  var end = item[side]["ts_end"]
  var duration = new Date(end) - new Date(start)
  new_item["id"] = id
  new_item["start"] = start
  new_item["end"] = end
  new_item["group"] = group
  new_item["className"] = 'stable-interval-one-cam';
  if (! item[side]["stable"]){
    new_item["className"] = 'unstable-interval';
  }
  new_item["content"] = item['id'].toString();
  new_item["title"] = createTooltip(item['id'].toString(), start, end, duration.toString(), item[side]["start_video_name"], item[side]["end_video_name"], item[side]["info"]);
  return new_item
}

var createLeftSideInterval = function(item, id, group){
  return createOneSideFromIntervalPair(item, id, group, "left")
}

var createRightSideInterval = function(item, id, group){
  return createOneSideFromIntervalPair(item, id, group, "right")
}

function setGroupName(item, id, group){
  var adj_item = item
  adj_item["group"] = group
  return adj_item
}
