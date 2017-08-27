var createTooltip = function(id, time_start, time_end, duration, filename_start, filename_end){
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
</table>"
  .replace("{index}", id)
  .replace("{time_start}", time_start)
  .replace("{time_end}", time_end)
  .replace("{duration}", duration)
  .replace("{filename_start}", filename_start)
  .replace("{filename_end}", filename_end)
return tooltip
}

var createSafeInterval = function(item, id, group){
  var new_item = {}
  var start = item["start_video_name"].split('--')[0].split('_')[2]
  var end = item["end_safe_video_name"].split('--')[1].slice(0, 27)
  var duration = new Date(end) - new Date(start)
  new_item["id"] = id
  new_item["group"] = group
  new_item["start"] = start
  new_item["end"] = end
  new_item["content"] = item["id"].toString()
  new_item["title"] = createTooltip(item["id"].toString(), start, end, duration.toString(), item["start_video_name"], item["end_safe_video_name"])
  if (item["id"] %2 === 0) {
    new_item["style"] = "background-color: rgb(75, 65, 65);border-color: rgb(255, 255, 255); color:rgb(255, 255, 255)";
  } else {
    new_item["style"] = "background-color: rgb(200, 198, 100);border-color:rgb(255, 255, 255); color:rgb(255, 255, 255)";
  }
  return new_item
}

var createUnsafeInterval = function(item, id, group){
  var new_item = {}
  var start = item["end_unsafe_video_name"].split('--')[0].split('_')[2]
  var end = item["end_unsafe_video_name"].split('--')[1].slice(0, 27)
  var duration = new Date(end) - new Date(start)
  new_item["id"] = id
  new_item["group"] = group
  new_item["start"] = start
  new_item["end"] = end
  new_item["content"] = item["id"].toString()
  new_item["title"] = createTooltip(item["id"].toString(), start, end, duration.toString(), item["start_video_name"], item["end_safe_video_name"])
  new_item["style"] = "background-color: rgb(255, 0, 0);border-color: rgb(255, 255, 255); color:rgb(255, 255, 255)";
  return new_item
}
