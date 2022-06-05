import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import React, { Component } from "react";
import { Button } from "@material-ui/core";

export default class ShowPlaylistPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      playlists: [],
      songs: [],
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
        this.setState({ playlists: data, songs: data.songs });
        console.log(data);
      });
  }

  render() {
    return (
      <Card >
        <Grid container spacing={2}  >
          {this.state.playlists.map((item) => {
            return (
              <Grid item xs={12} container style={{backgroundColor:"#AEF0D7"}} justifyContent="center">
                <Grid item xs={12} container >
                <Grid item xs={4}>
                    <img src={item.cover} height="200"/>
                  </Grid>

                  

                  <Grid item xs={6} >
                    <br/>
                    <h1>{item.name}</h1>
                    <h1>{item.owner}</h1>
                  </Grid>

                  <Grid item xs={2} >
                    <a href={"/recommendation/" + item.id}>a</a>
                  </Grid>
        
                </Grid>

                {item.songs?.map((items) => {
                  return (
                    
                    <Grid xs={8} justifyContent="center"  container direction="row-reverse" style={{backgroundColor:"#FFF",padding:"30px", borderStyle:"solid"}}>
                      
                      
                      <Grid item xs={3} align="center" style={{paddingTop:"20px"}}>
                        
                        <h1>{items.name}</h1>
                        
                        <h3>{items.artist}</h3>
                      </Grid>

                      <Grid item xs={3} >
                          <img src={items.img} width="131" style={{borderRadius:"50%"}} />
                        </Grid>
                      
                        
                    </Grid>
                    
                  );
                })}
              </Grid>
            );
          })}
        </Grid>
      </Card>
    );
  }
}

/*return this.state.playlists.map((item) => (
  <a href="http://127.0.0.1:8000/my-playlists/songs">
    <Card>
      <Grid container spacing={4} alignItems="center">
        <Grid item xs={12} align="center">
          <h1>{item.name}</h1>
          <br></br>
          <Grid item xs={8} align="center">
            <img src={item.cover} height="200px" width="200px" />
          </Grid>
        </Grid>
        <Grid item xs={12} align="center">
          <h1>{item.id}</h1>
        </Grid>
      </Grid>
      return {this.state.playlists.songs?.map(item => {
        <Grid container spacing={4} alignItems="center">
        <Grid item xs={12} align="center">
          <h1>{item.name}</h1>
          <br></br>
          <Grid item xs={8} align="center">
            <img src={item.img} height="200px" width="200px" />
          </Grid>
        </Grid>
        <Grid item xs={12} align="center">
          <h1>{item.artist}</h1>
        </Grid>
      </Grid>
      })})
    </Card>
  </a>
));*/
/*
render() {
  return (this.state.playlists.map((item) => (
    <a href="http://127.0.0.1:8000/my-playlists/songs">
      <Card>
        <h1>{item.name}</h1>
        <Card>
          {this.state.playlists.songs?.map((items) => {
            return (
              <Grid container spacing={4} alignItems="center">
                <Grid item xs={12} align="center">
                  <h1>{items.name}</h1>
                  <br></br>
                  <Grid item xs={8} align="center">
                    <img src={items.img} height="200px" width="200px" />
                  </Grid>
                </Grid>
                <Grid item xs={12} align="center">
                  <h1>{items.artist}</h1>
                </Grid>
              </Grid>
            );
          })}
        </Card>
      </Card>
    </a>
  )));
}*/
