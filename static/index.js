// to do: 
// get parse the html

var url = new URL('http://127.0.0.1:5000/request_html');
var list_url = new URL('http://127.0.0.1:5000/find_songs');

filterByNotEmpty = function filterByNotEmpty(elem){
	return elem != "";
}

const bruger = document.querySelector("#burger");
const playlistButton = document.querySelector("#PlaylistButton");
const playlistInput = document.querySelector("#playlistInput");
const nabarMenu = document.querySelector("#nav-links");
const messageBox = document.querySelector("#resultMessage");
const textNoticeForGetPlaylist = document.querySelector("#TextNoticeForGetPlaylist");
const privateDropDown = document.querySelector("#privateDropDown");
const descriptionTextarea = document.querySelector("#PlaylistDescriptionTextarea");
const playlistNameInput = document.querySelector("#PlaylistNameInput");
window.onload=function(){
        bruger.addEventListener('click', () => {
            nabarMenu.classList.toggle('is-active');
        })
    
        playlistButton.addEventListener('click',() => {
          if(playlistInput.value != "") {
            playlistButton.classList.toggle('is-loading');
            httpGetAsync(playlistInput.value, parseHtmlgetPlaylist);
          }
          else {
            playlistInput.classList.remove('is-danger');
            playlistInput.classList.add('is-danger');
            textNoticeForGetPlaylist.classList.toggle("is-hidden")
          }
        })
  }

  function httpGetAsync(i_theUrlGiven, i_callback)
  {
    url.searchParams.set('url', i_theUrlGiven);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
        i_callback(xmlHttp.responseText);
      }

    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
  }

  //TODO: after sending the list of songs function action

  doAfterSongListReturned = function(xmlHttpResponse){
    playlistButton.classList.toggle('is-loading')
    messageBox.classList.toggle('is-hidden');
    if(xmlHttpResponse.status == 200){
      playlistButton.classList.toggle('is-loading');
      messageBox.classList.toggle('is-hidden');
    }
  }

  function httpGetAsyncPostSongAlbumToServer(i_theUrlGiven, i_callback, i_content)
{
  var jsonToSend = new Object();
  jsonToSend.IsPrivate = privateDropDown.options[privateDropDown.selectedIndex].text == 'Yes' ? true : false; 
  jsonToSend.Description = descriptionTextarea.value;
  jsonToSend.PlaylistName = playlistNameInput.value;
  jsonToSend.SongList = i_content;
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() { 
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      i_callback(xmlHttp.responseText);
    }

  xmlHttp.open("POST", i_theUrlGiven, true);
  xmlHttp.setRequestHeader('Accept', 'application/json');
  xmlHttp.send(JSON.stringify(jsonToSend));
}



function MakeSongTableDynamically(formated_song_album_list) {
  const SongTableBody = document.querySelector("#SongTableBody");
  var size = formated_song_album_list.length
  for (let index = 0; index < size; index++) {
    SongTableBody.innerHTML += `
  <td>
    ${index}
  </td>
  <td>
    <label class="checkbox">
      <input type="checkbox" checked="checked">
      ${formated_song_album_list[index]}
    </label>
  </td>`
  }
}

  function parseHtmlgetPlaylist(i_appleHtmlText)
  {
  var htmlElement = document.createElement('html');
  htmlElement.innerHTML = i_appleHtmlText;
  console.log(htmlElement);
  song_artist = htmlElement.getElementsByClassName('song-name-wrapper');
  var song_album_searchQuery = [];
  var formated_song_album_list = [];
  for (var i=0 ; i < song_artist.length; i++) {
      song_album_searchQuery.push(song_artist[i].innerText);
  }

  for (var i=0 ; i < song_album_searchQuery.length; i++) {
    formated_song_album_list.push(song_album_searchQuery[i].split('\n').join(',').split(" ").join(",").split(",").filter(filterByNotEmpty).join(" "));
  }
  //console.log(formated_song_album_list);

  MakeSongTableDynamically(formated_song_album_list);
  httpGetAsyncPostSongAlbumToServer(list_url, doAfterSongListReturned, formated_song_album_list);
}




  // https://music.apple.com/il/playlist/wmai-idan/pl.u-RRbVYr2I3oNk0NK
  /*
            var content = document.createElement("div");
            content.className = "notification is-small";
            content.innerHTML += "This element cannot remain empty"
            inputAndButtonDiv.appendChild(content);
  */