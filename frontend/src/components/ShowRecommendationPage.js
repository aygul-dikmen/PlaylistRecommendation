import React, { Component } from "react";
import { Route, Link, Routes, useParams } from "react-router-dom";
import Card from "@material-ui/core/Card";
import Grid from "@material-ui/core/Grid";
class ShowRecommendationPage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      songs: [],
      id: this.props.params.id,
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
      <Grid
        container
        spacing={2}
        justifyContent="center"
        md={12}
      >
        <Grid
          container
          spacing={2}
          
          justifyContent="center"
          
        >
          {this.state.songs.map((item) => {
            return (
              <Grid
                item
                xl={12}
                container
                style={{ backgroundColor: "#88CF28" }}
                justifyContent="center"
              >
                <Card style={{"width":"600px"}}>
                  <Grid item xl={12} container spacing={2}>
                    <Grid item xl={4} style={{'float':'left'}}>
                      <img src={item.img} height="200" />
                    </Grid>

                    <Grid item xl={8} style={{'justifyContent':'center'}}>
                      <br />
                      <h1>{item.name}</h1>
                      <h1>{item.artist}</h1>
                    </Grid>
                  </Grid>
                </Card>
              </Grid>
            );
          })}

          <Grid
            item
            xs={12}
            style={{ "margin": "auto" , "alignItems":"center",
            "justifyContent":"center", "paddingLeft": "500px", "backgroundColor": "#88CF28"}}
          >
            <div
              class="ui buttons"
              
            >
              <button class="huge ui red button" onClick={() => window.location.replace('http://127.0.0.1:8000/spotify/delete-playlist','_self')}>Not my cup of tea</button>
              <div class="huge or"></div>
              <button class="huge ui yellow button" onClick={() => window.open('http://127.0.0.1:8000/my-playlists', '_self')}>Yes, keep it</button>
            </div>
          </Grid> 
        </Grid>
      </Grid>
    );
  }
}

export default (props) => (
  <ShowRecommendationPage {...props} params={useParams()} />
);

/*{
      
      this.state.songs.map((item) => {
        return <h1>{item.name}</h1>;
      });

    }
  }*/
