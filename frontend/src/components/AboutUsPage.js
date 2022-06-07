import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import React, { Component } from "react";
import { Typography } from "@material-ui/core";
import { IconButton } from "@material-ui/core";
import GitHub from '@material-ui/icons/GitHub';
import Email from '@material-ui/icons/Email';
import LinkedIn from '@material-ui/icons/LinkedIn';

const styles = {
  gridContainer: {
    backgroundImage:
      "url('https://images.pexels.com/photos/8186273/pexels-photo-8186273.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')",
    "height": "1200px",
    "background-repeat": "no-repeat",
    "background-size": "cover",
    justifyContent: "center",
  },
  gridItem: {
    height: "400px",
    width: "800px",
    margin: "auto",
    justifyContent: "center",
    alignItems: "center",
    padding: "40px",
    paddingTop: "80px",
    paddingLeft: "80px"
  },
};

export default class ShowPlaylistPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      playlists: [],
    };
  }

  render() {
    return (
      <Grid
        container
        spacing={4}
        xl={12}
        direction="row"
        style={styles.gridContainer}
      >
        <Grid item xs={8} style={{paddingTop:"80px"}}>
          <Card style={styles.gridItem}>
          <Grid container spacing={3} xs={10} direction="row">
              <Grid item xs={6}>
                <img 
                  src="/frontend/src/static/images/aygül_vesikalık.jpeg"
                  height={250}
                  width={200}
                />
              </Grid>
              <Grid item xs={6} style={{paddingLeft: "100px"}}>
                
                <Typography
                  align="center"
                  style={{ paddingTop: "10px", fontSize: "24px" }}
                >
                  Aygül Dikmen
                </Typography>
                <hr/>
                <Typography align="center">
                  Hey, I am a senior student in Computer Engineering at Çukurova
                  University. Currently I've been interested in Machine Learning.
                </Typography>
                <hr/>
                <IconButton onClick={() => window.open('https://github.com/aygul-dikmen', '_blank')}>
                  <GitHub fontSize="large"/>
                </IconButton>
                <a href="mailto:ayguldikmen@gmail.com" target="_top"><IconButton >
                  <Email fontSize="large"/>
                </IconButton></a>
                <IconButton onClick={() => window.open('https://www.linkedin.com/in/aygul-dikmen-b5b42b172/', '_blank')}>
                  <LinkedIn fontSize="large"/>
                </IconButton>
              </Grid>
            </Grid>
          </Card>
        </Grid>
        <Grid item xs={8} direction="row">
          <Card style={styles.gridItem}>
            <Grid container spacing={3} xs={10} direction="row">
              <Grid item xs={6}>
                <img
                  src="/frontend/src/static/images/vesikalık.jpeg"
                  height={250}
                  width={200}
                />
              </Grid>
              <Grid item xs={6} style={{paddingLeft: "100px"}}>
                
                <Typography
                  align="center"
                  style={{ paddingTop: "10px", fontSize: "24px" }}
                >
                  Büşra Oran
                </Typography>
                <hr/>
                <Typography align="center">
                  Hey, I am a senior student in Computer Engineering at Çukurova
                  University. Currently I've been interested in Web development.
                </Typography>
                <hr/>
                <IconButton onClick={() => window.open('https://github.com/busraaaoran', '_blank')}>
                  <GitHub fontSize="large"/>
                </IconButton>
                <a href="mailto:busraoran043@gmail.com" target="_top"><IconButton >
                  <Email fontSize="large"/>
                </IconButton></a>
                
                <IconButton onClick={() => window.open('https://www.linkedin.com/in/busraoran/', '_blank')}>
                  <LinkedIn fontSize="large"/>
                </IconButton>
              </Grid>
            </Grid>
          </Card>
        </Grid>
      </Grid>
    );
  }
}

