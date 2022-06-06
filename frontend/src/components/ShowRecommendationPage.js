import React, { Component } from "react";
import {Route, Link, Routes, useParams} from 'react-router-dom';
import Card from "@material-ui/core/Card";
import Grid from "@material-ui/core/Grid";
class ShowRecommendationPage extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
      songs: [],
      id: this.props.params.id
    };
    console.log("deneme");
    this.getPlaylistSongs = this.getPlaylistSongs.bind(this);
    this.getPlaylistSongs();
  }

  getPlaylistSongs() {
    fetch("/spotify/get-recommendation/" + this.state.id)
      .then((response) => {
        if (!response.ok) {
          console.log("aaaa");
          return {};
        } else {
          console.log("bbb");
          return response.json();
        }
      })
      .then((data) => {
        this.setState({ songs: data });
        console.log(data);
      });
  }

  render() {
    return (
      <Card >
        <Grid container spacing={2}  >
          {this.state.songs.map((item) => {
            return (
              <Grid item xs={12} container style={{backgroundColor:"#AEF0D7"}} justifyContent="center">
                <Grid item xs={12} container >
                <Grid item xs={4}>
                  <img src={item.img} height="200"/>
                  </Grid>

                  <Grid item xs={6} >
                    <br/>
                    <h1>{item.name}</h1>
                    <h1>{item.artist}</h1>
                  </Grid>
        
                </Grid>
              </Grid>
            );
          })}
        </Grid>
      </Card>
    );
  }
}

export default(props) => (
  <ShowRecommendationPage
  {...props}
  params = {useParams()} />
);

/*{
      
      this.state.songs.map((item) => {
        return <h1>{item.name}</h1>;
      });

    }
  }*/