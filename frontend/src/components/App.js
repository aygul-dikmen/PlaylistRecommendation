import React, { Component } from "react";
import {render} from "react-dom";
import HomePage from "./HomePage";
import ShowPlaylistPage from "./ShowPlaylistPage";
import ShowRecommendationPage from "./ShowRecommendationPage";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

export default class App extends Component{
    constructor(props){
        super(props);
         
    }
    render(){
        return(<Router>
          <Routes>
            <Route exact path='/' element={<HomePage />} />
            <Route path='/my-playlists' element={<ShowPlaylistPage />} />
            <Route path='/recommendation' element={<ShowRecommendationPage />} />
          </Routes>
          </Router>
      );
    }

}

const appDiv = document.getElementById("app");
render(<App />, appDiv);