import React, { Component } from "react";
import ShowPlaylistPage from "./ShowPlaylistPage";
import ShowRecommendationPage from "./ShowRecommendationPage";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import { FormControl } from "@material-ui/core";
import { Radio } from "@material-ui/core";
import { RadioGroup } from "@material-ui/core";
import { FormControlLabel } from "@material-ui/core";
import  Paper  from "@material-ui/core/Paper";
import Image from '../../static/images/bg.jpg';

const styles = {
  gridContainer: {
      backgroundImage: "url('https://images.unsplash.com/photo-1622867500182-5670d5a2c8e2?ixlib=rb-1.2.1&raw_url=true&q=80&fm=jpg&crop=entropy&cs=tinysrgb&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774')",
      "height": "1000px",
      'background-repeat': 'no-repeat',
      'background-size': 'cover',
  }
};

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      spotifyAuthenticated: false,
    };
    this.authenticateSpotify = this.authenticateSpotify.bind(this);
    //this.authenticateSpotify();
  }

  authenticateSpotify() {
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotifyAuthenticated: data.status });
        console.log(data.status);
        if (!data.status) {
          fetch("/spotify/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      });
  }

  render() {
    return (
      <Grid container spacing={4} style={styles.gridContainer} >
        <Grid item xs={12} align="center" style={{'margin-top': "250px"}}>
          <Typography component="h4" variant="h4" style={{color:"#FFFFFF", "margin-bottom": "50px"}}>
            SPOTIFY PLAYLIST RECOMMENDATION SYSTEM
          </Typography>
          <Button
            style={{
              backgroundColor: "#17682C",
              padding: "18px 36px",
              fontSize: "18px",
              color: "#FFFFFF",
            }}
            variant="contained"
            onClick={this.authenticateSpotify}
          >
            Login with Spotify
          </Button>
        
          
          
        </Grid>
        
      </Grid>
      
    );
  }
}
