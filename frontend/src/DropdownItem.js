import React from 'react';

function Dropdown(){

    const {show,setShow} = useState(false);

    return(
        <div className="dropdown">
            <div className="dropdown-btn">Playlist item</div>
            <div className="dropdown-content">
                this is content area
            </div>
        </div>
    )
}

export default Dropdown;