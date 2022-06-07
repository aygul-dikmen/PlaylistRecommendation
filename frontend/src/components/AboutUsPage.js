import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import React, { Component } from "react";
import Paper from "@material-ui/core/Paper";
import { Typography } from "@material-ui/core";
import Facebook from "@material-ui/icons/Facebook";
import { Icon } from "@material-ui/core";
import GitHub from '@material-ui/icons/GitHub';
import Email from '@material-ui/icons/Email';
import YouTube from '@material-ui/icons/YouTube';
import LinkedIn from '@material-ui/icons/LinkedIn';

const styles = {
  gridContainer: {
    backgroundImage:
      "url('https://images.pexels.com/photos/3063362/pexels-photo-3063362.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')",
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
                <Icon style={{paddingLeft:"10px"}}>
                  <Facebook fontSize="large"/> 
                </Icon>
                <Icon>
                  <GitHub fontSize="large"/>
                </Icon>
                <Icon>
                  <Email fontSize="large"/>
                </Icon>
                <Icon>
                  <YouTube fontSize="large"/>
                </Icon>
                <Icon>
                  <LinkedIn fontSize="large"/>
                </Icon>
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
                <Icon style={{paddingLeft:"10px"}}>
                  <Facebook fontSize="large"/> 
                </Icon>
                <Icon>
                  <GitHub fontSize="large"/>
                </Icon>
                <Icon>
                  <Email fontSize="large"/>
                </Icon>
                <Icon>
                  <YouTube fontSize="large"/>
                </Icon>
                <Icon>
                  <LinkedIn fontSize="large"/>
                </Icon>
              </Grid>
            </Grid>
          </Card>
        </Grid>
      </Grid>
    );
  }
}

/*<Paper elevation={3} style={{display:'flex', justifyContent:'center', backgroundColor:"#AEF0D7"}}>
        <Grid container spacing={2} xs={12} alignItems="center"  style={{display:'flex', justifyContent:'center', backgroundColor:"#AEF0D7"}}>
        <Grid item style={{
              alignItems: "center",
              justifyContent: "center",
             
            }}>
          <Card
            style={{
              height: "400px",
              width: "800px",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            Büşra
          </Card>
        </Grid>
        <Grid item style={{
              alignItems: "center",
              justifyContent: "center",
            }}>
          <Card style={{ height: "400px", width: "800px" }}>Aygül</Card>
        </Grid>
        </Grid>
      </Paper>*/
