import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from 'react-redux';
import AuthFormBlock from '../../components/auth/AuthFormBlock';
import { changeInputs, formError, initializeForm, register } from '../../modules/auth';
import { withRouter } from 'react-router-dom';

function RegisterForm({ history }) {
    const dispatch = useDispatch();
    const { form, authError } = useSelector(({ auth }) => ({
        form: auth.register,
        auth: auth.auth,
        authError: auth.authError
    }));

    const onChange = (e) => {
        const { name, value } = e.target;
        dispatch(
            changeInputs({
                type: 'register',
                key: name,
                value,
            }),
        );
    };

    const onSubmit = e => {
        e.preventDefault();
        console.log("onsubmit 호출");
        const { email, password, password_check, fullname } = form;
        console.log(email, password, password_check, fullname);
        if (!email || !password || !password_check || !fullname) {
            dispatch(formError("모든 값을 채워야합니다."))
            return
        }
        if (password !== password_check) {
            dispatch(formError("비밀번호와 비밀번호 확인이 다릅니다."))
            return;
        }
        dispatch(register({ email, password, fullname })).payload
            .then(res => {
                console.log(res);
                if (res.register_success) {
                    history.push('/login');
                    return { register_success: true }
                }
                else {
                    dispatch(formError("이미 등록된 Email입니다."))
                    return { register_success: false }
                }
            })
    };

    useEffect(() => {
        dispatch(initializeForm('register'));
        dispatch(formError(''));
    }, [dispatch]);

    return (
        <AuthFormBlock
            type="register"
            form={form}
            onChange={onChange}
            onSubmit={onSubmit}
            error={authError}
        />
    );
}

RegisterForm.propTypes = {
    history: PropTypes.object
}

export default withRouter(RegisterForm)
