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
        style={{ margins: "auto" }}
        justifyContent="center"
        
      >
        <Grid
          container
          spacing={2}
          style={{ margins: "auto" }}
          justifyContent="center"
          
        >
          {this.state.songs.map((item) => {
            return (
              <Grid
                item
                xs={12}
                container
                style={{ backgroundColor: "#AEF0D7" }}
                justifyContent="center"
              >
                <Card >
                  <Grid item xs={12} container >
                    <Grid item xs={4} style={{'margin':'auto'}}>
                      <img src={item.img} height="200" />
                    </Grid>

                    <Grid item xs={8} justifyContent="flex-end">
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
            style={{ margin: "auto" }}
            alignItems="center"
            justifyContent="center"
          >
            <div
              class="ui buttons"
              style={{ alignItems: "center", justifyContent: "center" }}
            >
              <button class="ui red button">Not my cup of tea</button>
              <div class="or"></div>
              <button class="ui green button">Yes, keep it</button>
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
