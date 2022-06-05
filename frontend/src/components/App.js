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
import AboutUsPage from "./AboutUsPage";

export default class App extends Component{
    constructor(props){
        super(props);
         
    }
    render(){
        return(<Router>
          <Routes>
            <Route exact path='/' element={<HomePage />} />
            <Route path='/my-playlists' element={<ShowPlaylistPage />} />
            <Route path='/recommendation/:id' element={<ShowRecommendationPage />} />
            <Route path='/about-us' element={<AboutUsPage />} />
          </Routes>
          </Router>
      );
    }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);