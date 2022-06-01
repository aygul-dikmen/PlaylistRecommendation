import React, { Component } from "react";

export default class ShowSongsPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      songs: [],
    };
    this.getPlaylistSongs = this.getPlaylistSongs.bind(this);
    this.getPlaylistSongs();
  }

  getPlaylistSongs() {
    fetch("/spotify/songs")
      .then((response) => {
        if (!response.ok) {
          return {};
        } else {
          return response.json();
        }
      })
      .then((data) => {
        this.setState({ songs: data });
        console.log(data);
      });
  }
  
  render() {
    return (<h1>{this.state.songs.total}</h1>) ;
  }
}
