import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import React, { Component } from "react";
import Paper from "@material-ui/core/Paper";
import { Typography } from "@material-ui/core";


const styles = {
  gridContainer: {
      backgroundImage: "url('https://images.unsplash.com/photo-1557672211-0741026eacfb?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=870&q=80')",
      "height": "1000px",
      'background-repeat': 'no-repeat',
      'background-size': 'cover'
  },
  gridItem: {
    "height": "400px",
    "width": "600px",
    "margin": "auto",
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
      <Grid container spacing={2} xs={12} justifyContent='center' direction="row" alignItems="center" style={styles.gridContainer}>
        <Grid item xs={8} ><Card style={styles.gridItem}><Typography align="center">Aygül</Typography></Card></Grid>
        <Grid item xs={8} ><Card style={styles.gridItem}><Typography align="center">Büşra</Typography></Card></Grid>
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