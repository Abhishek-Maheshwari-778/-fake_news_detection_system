import {React} from "react";

import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';

import  { LinkContainer } from 'react-router-bootstrap';

function Header(props) {

    const { activeContainer } = props;

    return (
        <header>
            <Container>
                <Navbar bg="" expand="lg">
                    <Container>
                        <LinkContainer to='/'>
                            <Navbar.Brand href="/">
                                <img src={process.env.PUBLIC_URL + '/logo.png'} height={35} className='logo-image' alt="Logo"></img>
                                <span style={{fontWeight: 600, color: '#136996'}}>Fake News</span> <span style={{color: '#48a2f8'}}>Detection System</span>
                            </Navbar.Brand>
                        </LinkContainer>
                        <Navbar.Toggle aria-controls="hearder-navbar" />
                        <Navbar.Collapse id="hearder-navbar" className="justify-content-end">
                            <Nav>
                                <LinkContainer to='/checkbytitle'>
                                    <Nav.Link className={activeContainer === 2 ? 'active-link' : 'inactive-link'}>
                                        <div>
                                            <li>
                                                <div>Check News By Title</div>
                                            </li>
                                        </div>
                                    </Nav.Link>
                                </LinkContainer>
                            </Nav>
                            <Nav>
                                <LinkContainer to='/newsquiz'>
                                    <Nav.Link className={activeContainer === 3 ? 'active-link' : 'inactive-link'}>
                                        <div>
                                            <li>
                                                <div>News Quiz</div>
                                            </li>
                                        </div>
                                    </Nav.Link>
                                </LinkContainer>
                            </Nav>
                        </Navbar.Collapse>
                    </Container>
                </Navbar>
            </Container>
        </header>
    )
};

export default Header;
