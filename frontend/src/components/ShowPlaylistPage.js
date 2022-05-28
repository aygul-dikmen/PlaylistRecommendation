import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import React, { Component } from "react";

export default class ShowPlaylistPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      playlists: [],
    };
    this.getUserPlaylists = this.getUserPlaylists.bind(this);
    this.getUserPlaylists();
  }

  getUserPlaylists() {
    fetch("/spotify/pl")
      .then((response) => {
        if (!response.ok) {
          return {};
        } else {
          return response.json();
        }
      })
      .then((data) => {
        this.setState({playlists : data});
        console.log(data);
      });
  }

  render() {
    
    return this.state.playlists.map((item) => (
      <Card>
        <Grid container spacing={4} alignItems="center">
          <Grid item xs={12} align="center">
            <h1>{item.name}</h1>
            <br></br>
            <Grid item xs={8} align="center">
              <img
                src={item.cover}
                height="200px"
                width="200px"
              />
            </Grid>
          </Grid>
          <Grid item xs={12} align="center">
            <h1>{item.id}</h1>
          </Grid>
        </Grid>
      </Card>
    ));
  }
}
