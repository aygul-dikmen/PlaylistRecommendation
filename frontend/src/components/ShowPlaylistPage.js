import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import React, { Component } from "react";

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
      <Card>
        <Grid container spacing={2}>
          {this.state.playlists.map((item) => {
            return (
              <Grid
                item
                xs={12}
                container
                spacing={2}
                style={{ backgroundColor: "#88CF28" }}
                justifyContent="center"
              >
                <Grid item xs={12} container>
                  <Grid item xs={4}>
                    <img
                      src={item.cover}
                      height="200"
                      style={{ borderRadius: "10px" }}
                    />
                  </Grid>

                  <Grid item xs={6}>
                    <br />
                    <h1>{item.name}</h1>
                    <h1>{item.owner}</h1>
                  </Grid>

                  <Grid item xs={2} style={{ margin: "auto" }}>
                    <a href={"/recommendation/" + item.id}>
                      <button class="ui huge orange button">
                        Show my recommendation
                      </button>
                    </a>
                  </Grid>
                </Grid>

                {item.songs?.map((items) => {
                  return (
                    <Grid
                      xs={8}
                      justifyContent="center"
                      container
                      direction="row-reverse"
                      style={{
                        backgroundColor: "#FFF",
                        padding: "30px",
                        borderStyle: "solid",
                        borderColor: "#88CF28",
                        borderRadius: "10px",
                      }}
                    >
                      <Grid
                        item
                        xs={3}
                        align="center"
                        style={{ paddingTop: "20px" }}
                      >
                        <h1>{items.name}</h1>

                        <h3>{items.artist}</h3>
                      </Grid>

                      <Grid item xs={3}>
                        <img
                          src={items.img}
                          width="131"
                          style={{ borderRadius: "50%" }}
                        />
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
