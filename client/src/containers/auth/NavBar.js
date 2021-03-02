import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { logout } from '../../modules/auth';
import { withRouter } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { getCookie } from '../../lib/apis/client';
import { getUser } from '../../lib/apis/auth';
import { Nav, Navbar, Alert } from 'react-bootstrap';

function NavBar({ history }) {
    const { id, fullname } = {
        id: sessionStorage.getItem('id'),
        fullname: sessionStorage.getItem('fullname'),
    };
    // const [user, setUser] = useState(null);
    const [error, setError] = useState(null);
    const dispatch = useDispatch();
    const onClick = (e) => {
        e.preventDefault();
        dispatch(logout());
    };
    // const catchUser = () => ({
    //     id: localStorage.getItem('id'),
    //     fullname: localStorage.getItem('fullname'),
    // });
    const resetUser = async () => {
        try {
            const res = await getUser();
            console.log(res.data.user);
            // setUser(res.data.user);
            const { id, fullname } = res.data.user;
            console.log(id, fullname);
            sessionStorage.setItem('id', id);
            sessionStorage.setItem('fullname', fullname);
        } catch (err) {
            console.log(err.response.data);
            setError(err.response.msg);
            sessionStorage.clear();
            dispatch(logout());
            history.push('/');
        }
    };
    useEffect(() => {
        if (!getCookie('csrf_access_token')) {
            // setUser(null);
            sessionStorage.clear();
        } else if (!id || !fullname) {
            resetUser();
        }
    }, [id, fullname]);
    return (
        <>
            {error && <Alert variant="fail">{error}</Alert>}
            <Navbar fixed="top" expand="lg" variant="light" bg="light">
                <Navbar.Brand href="/">
                    <img
                        alt=""
                        src="https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fc90d82c1-277a-42a3-9e93-5624f3bff5d3%2FKDT_12x.png?table=block&id=fba44647-7b62-42b5-93a5-c3fdfb8d0187&width=250&userId=479b5c03-3ace-4f65-938c-026795f1021d&cache=v2"
                        width="30"
                        height="30"
                        className="d-inline-block align-top"
                    />{' '}
                    <b>Racer Portfolio</b>
                </Navbar.Brand>
                <Nav>
                    <Nav.Link href="/network">Network</Nav.Link>
                </Nav>
                <Navbar.Collapse className="justify-content-end">
                    <Nav>
                        {!id || !fullname ? (
                            <>
                                <Nav.Link href="/login">Login</Nav.Link>
                                <Nav.Link href="/register">Register</Nav.Link>
                            </>
                        ) : (
                            <>
                                {id && fullname && (
                                    <Nav.Link
                                        href={'/portfolio/' + id}
                                        style={{ fontWeight: 'bold' }}
                                    >
                                        {fullname}
                                    </Nav.Link>
                                )}
                                <Nav.Link href="" onClick={onClick}>
                                    Logout
                                </Nav.Link>
                            </>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        </>
    );
}

NavBar.propTypes = {
    history: PropTypes.object,
    user: PropTypes.any,
    setUser: PropTypes.func,
};
export default withRouter(NavBar);
