// to do: 
// get parse the html

const url = new URL('http://127.0.0.1:5000/request_html');
const list_url = new URL('http://127.0.0.1:5000/find_songs');


filterByNotEmpty = function filterByNotEmpty(elem){
	return elem != "";
}

class SongSlectedCounter {
  constructor(i_selectedDOMElem, i_NumberOfSelected) {
    this.SelectedDOMElem = i_selectedDOMElem;
    this.NumberOfSelected = i_NumberOfSelected;
  }

  IncSelectedNumber(){
    this.NumberOfSelected++;
    this.SelectedDOMElem.textContent = 'Selected: ' + this.NumberOfSelected;
  }

  DecSelectedNumber(){
    this.NumberOfSelected--;
    this.SelectedDOMElem.textContent = 'Selected: ' + this.NumberOfSelected;
  } 

  updateSelected(i_nubmer_of_Checked){
    this.SelectedDOMElem.textContent = 'Selected: ' + i_nubmer_of_Checked;
  }
}

const bruger = document.querySelector("#burger");
const playlistInput = document.querySelector("#playlistInput");
const nabarMenu = document.querySelector("#nav-links");
const messageBox = document.querySelector("#resultMessage");
const textNoticeForGetPlaylist = document.querySelector("#TextNoticeForGetPlaylist");
const privateDropDown = document.querySelector("#privateDropDown");
const descriptionTextarea = document.querySelector("#PlaylistDescriptionTextarea");
const playlistNameInput = document.querySelector("#PlaylistNameInput");

const prevStageButton = document.querySelector("#prevStage");
const nextStageButton = document.querySelector("#nextStage");

const stage1 = document.querySelector("#step1");
const stage2 = document.querySelector("#step2");
const stage3 = document.querySelector("#step3");
const stage4 = document.querySelector("#step4");

const inputCardField = document.querySelector("#InputCardField");

const playlistDescription = document.querySelector("#PlaylistDescription");
const playlistNameField = document.querySelector("#playlistNameField"); 
const privateSettingDropdown = document.querySelector("#privateSettingDropdown"); 
const getPlaylistFields = document.querySelector("#getPlaylistFields");
const numberOfSelectedSongs = document.querySelector("#NumberOfSelectedSongs");
const modalCloseButton = document.querySelector("#modalCloseButton");
const tableModal = document.querySelector("#tableModal");
const SongTableBody = document.querySelector("#SongTableBody");
const totalNumberOfSongs = document.querySelector("#TotalNumberOfSongs");
const saveChangesButton = document.querySelector("#SaveChangesButton");
const canselPlaylistButton = document.querySelector("#CanselPlaylistButton");
const SelectedSongsInCheckBox = new SongSlectedCounter(numberOfSelectedSongs, 0);

const ShowAfterPlaylistImport = document.querySelector("#ShowAfterPlaylistImport");
const successfullPlaylistImport = document.querySelector("#successfullPlaylistImport");
const failedPlaylistImport = document.querySelector("#failedPlaylistImport");
const BeforeImport = document.querySelector("#BeforeImport");

doAfterSongListReturned = function(xmlHttpResponse){
  const playlistButton = document.getElementById("playlistButton");
  console.log(xmlHttpResponse)
  tableModal.classList.toggle('is-active');
  saveChangesButton.classList.toggle('is-loading');
  playlistButton.classList.toggle('is-loading');
  BeforeImport.classList.toggle('is-hidden');
  ShowAfterPlaylistImport.classList.toggle('is-hidden');
  if(xmlHttpResponse.status ==200){
   successfullPlaylistImport.classList.toggle('is-hidden');
   newPlaylistAncor = document.querySelector("#newPlaylistAncor");
   newPlaylistAncor.href = xmlHttpResponse.responseText;
  }
  else {
    failedPlaylistImport.classList.toggle('is-hidden');
  }
}



window.onload=function(){
        const playlistButton = document.getElementById("playlistButton");


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
            textNoticeForGetPlaylist.classList.toggle("is-hidden");
          }
        })

        prevStageButton.addEventListener('click', () => {
          if(stage2.classList.contains('is-active'))
          {
            stage2.classList.toggle('is-active');
            stage1.classList.toggle('is-active');
            playlistDescription.classList.toggle('is-hidden');
            playlistNameField.classList.toggle('is-hidden');
          }
          else if(stage3.classList.contains('is-active'))
          {
            stage3.classList.toggle('is-active');
            stage2.classList.toggle('is-active');
            privateSettingDropdown.classList.toggle('is-hidden');
            playlistDescription.classList.toggle('is-hidden');
          }
          else if(stage4.classList.contains('is-active'))
          {
            stage4.classList.toggle('is-active');
            stage3.classList.toggle('is-active');
            getPlaylistFields.classList.toggle('is-hidden');
            privateSettingDropdown.classList.toggle('is-hidden');
            playlistButton.classList.toggle('is-hidden');
            nextStageButton.classList.toggle('is-hidden');
          }
        })

        nextStageButton.addEventListener('click', () => {
          if(stage1.classList.contains('is-active'))
          {
            stage1.classList.toggle('is-active')
            stage2.classList.toggle('is-active')
            playlistNameField.classList.toggle('is-hidden')
            playlistDescription.classList.toggle('is-hidden');
          }
          else if(stage2.classList.contains('is-active'))
          {
            stage2.classList.toggle('is-active')
            stage3.classList.toggle('is-active')
            playlistDescription.classList.toggle('is-hidden');
            privateSettingDropdown.classList.toggle('is-hidden');
          }
          else if(stage3.classList.contains('is-active'))
          {
            stage3.classList.toggle('is-active')
            stage4.classList.toggle('is-active')
            privateSettingDropdown.classList.toggle('is-hidden');
            getPlaylistFields.classList.toggle('is-hidden');
            playlistButton.classList.toggle('is-hidden');
            nextStageButton.classList.toggle('is-hidden');
          }
        })

        modalCloseButton.addEventListener('click' , () => {
          tableModal.classList.toggle('is-active');
        })

        canselPlaylistButton.addEventListener('click' , () => {
          tableModal.classList.toggle('is-active');
          playlistButton.classList.toggle('is-loading');
        })

        saveChangesButton.addEventListener('click' , () => {
          var localcheckboxList = document.getElementsByClassName("checkbox");
          var finalSongList = [];
          saveChangesButton.classList.toggle('is-loading')
          for (let index = 0; index < localcheckboxList.length; index++) {
            if(localcheckboxList[index].control.checked)
            finalSongList.push(localcheckboxList[index].innerText)
          }
          playlistButton.classList.toggle('is-loading');
          httpGetAsyncPostSongAlbumToServer(list_url, doAfterSongListReturned, finalSongList);
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
      i_callback(xmlHttp);
    }

  xmlHttp.open("POST", i_theUrlGiven, true);
  xmlHttp.setRequestHeader('Accept', 'application/json');
  xmlHttp.send(JSON.stringify(jsonToSend));
}

function checkIfCheckedfunc(checkBoxChanged) {
  if (checkBoxChanged.control.checked) {
    SelectedSongsInCheckBox.IncSelectedNumber();
  } else {
    SelectedSongsInCheckBox.DecSelectedNumber();
  }
}

function MakeSongTableDynamically(formated_song_album_list) {
  tableModal.classList.toggle('is-active');

  var size = formated_song_album_list.length
  var index = 0
  for (index = 0; index < size; index++) {
    SongTableBody.innerHTML += `
  <td>
    ${index + 1}
  </td>
  <td>
    <label class="checkbox">
      <input type="checkbox" checked="checked">
      ${formated_song_album_list[index]}
    </label>
  </td>`
  }
  var localcheckboxList = document.getElementsByClassName("checkbox");
  SelectedSongsInCheckBox.NumberOfSelected = localcheckboxList.length;
  totalNumberOfSongs.textContent = 'Total: ' + index;
  numberOfSelectedSongs.textContent = 'Selected ' + index;

  for (let index = 0; index < localcheckboxList.length; index++) {
    localcheckboxList[index].addEventListener('change', () => {
      checkIfCheckedfunc(localcheckboxList[index]);
    });
  }
}

  function parseHtmlgetPlaylist(i_appleHtmlText)
  {
  var htmlElement = document.createElement('html');
  htmlElement.innerHTML = i_appleHtmlText;
  song_artist = htmlElement.getElementsByClassName('song-name-wrapper');
  var song_album_searchQuery = [];
  var formated_song_album_list = [];
  for (var i=0 ; i < song_artist.length; i++) {
      song_album_searchQuery.push(song_artist[i].innerText);
  }

  for (var i=0 ; i < song_album_searchQuery.length; i++) {
    formated_song_album_list.push(song_album_searchQuery[i].split('\n').join(',').split(" ").join(",").split(",").filter(filterByNotEmpty).join(" "));
  }

  MakeSongTableDynamically(formated_song_album_list);
}


  // https://music.apple.com/il/playlist/wmai-idan/pl.u-RRbVYr2I3oNk0NK