import React, { useState, useEffect } from 'react';
import './AppointmentForm.css';
import Modal from '../Modal/Modal';

function AppointmentForm ()
{
        const [ formData, setFormData ]=useState( {
                patient_name: '',
                age: '',
                mobile: '',
                doctor_id: '',
                disease: '',
                appointment_date: '',
                appointment_time: '',
                email: ''
        } );

        const [ doctors, setDoctors ]=useState( [] );
        const [ isModalOpen, setIsModalOpen ]=useState( false );
        const [ modalMessage, setModalMessage ]=useState( '' );

        useEffect( () =>
        {
                // Fetch doctors when component mounts
                fetch( '/api/doctors' )
                        .then( response => response.json() )
                        .then( data => setDoctors( data ) )
                        .catch( error => console.error( 'Error fetching doctors:', error ) );

                // Botpress scripts
                const script1=document.createElement( 'script' );
                script1.src="https://cdn.botpress.cloud/webchat/v2/inject.js";
                script1.async=true;
                document.body.appendChild( script1 );

                const script2=document.createElement( 'script' );
                script2.src="https://mediafiles.botpress.cloud/37dc6043-18cd-49ec-9088-37150adec087/webchat/v2/config.js";
                script2.async=true;
                document.body.appendChild( script2 );

                return () =>
                {
                        document.body.removeChild( script1 );
                        document.body.removeChild( script2 );
                };
        }, [] );

        const handleChange=( e ) =>
        {
                setFormData( {
                        ...formData,
                        [ e.target.name ]: e.target.value
                } );
        };

        const handleSubmit=( e ) =>
        {
                e.preventDefault();

                const appointmentData={
                        ...formData,
                        appointment_date: `${ formData.appointment_date }T${ formData.appointment_time }`,
                        status: 'Confirmed'
                };

                fetch( '/api/add-appointment', {
                        method: 'POST',
                        headers: {
                                'Content-Type': 'application/json'
                        },
                        body: JSON.stringify( appointmentData )
                } )
                        .then( response => response.json() )
                        .then( data =>
                        {
                                if ( data.success )
                                {
                                        setModalMessage( "Appointment booked successfully!" );
                                        setIsModalOpen( true );
                                        // Reset form
                                        setFormData( {
                                                patient_name: '',
                                                age: '',
                                                mobile: '',
                                                doctor_id: '',
                                                disease: '',
                                                appointment_date: '',
                                                appointment_time: '',
                                                email: ''
                                        } );
                                } else
                                {
                                        setModalMessage( "Error booking appointment: "+data.error );
                                        setIsModalOpen( true );
                                }
                        } )
                        .catch( error =>
                        {
                                setModalMessage( "Error: "+error );
                                setIsModalOpen( true );
                        } );
        };

        const closeModal=() =>
        {
                setIsModalOpen( false );
        };

        return (
                <div className="appointment-form">
                        <div className="form-container">
                                <h2>Book An Appointment</h2>
                                <form onSubmit={ handleSubmit }>
                                        <div className="form-row">
                                                <div className="form-group">
                                                        <label htmlFor="patient_name">Your Name*</label>
                                                        <input type="text" id="patient_name" name="patient_name" required value={ formData.patient_name } onChange={ handleChange } />
                                                </div>
                                                <div className="form-group">
                                                        <label htmlFor="age">Age*</label>
                                                        <input type="number" id="age" name="age" required value={ formData.age } onChange={ handleChange } />
                                                </div>
                                                <div className="form-group">
                                                        <label htmlFor="mobile">Mobile No.*</label>
                                                        <input type="tel" id="mobile" name="mobile" required value={ formData.mobile } onChange={ handleChange } />
                                                </div>
                                        </div>
                                        <div className="form-row">
                                                <div className="form-group">
                                                        <label htmlFor="appointment_date">Select Date*</label>
                                                        <input type="date" id="appointment_date" name="appointment_date" required value={ formData.appointment_date } onChange={ handleChange } />
                                                </div>
                                                <div className="form-group">
                                                        <label htmlFor="appointment_time">Time*</label>
                                                        <input type="time" id="appointment_time" name="appointment_time" required value={ formData.appointment_time } onChange={ handleChange } />
                                                </div>
                                                <div className="form-group">
                                                        <label htmlFor="email">Email</label>
                                                        <input type="email" id="email" name="email" value={ formData.email } onChange={ handleChange } />
                                                </div>
                                        </div>
                                        <div className="form-group">
                                                <label htmlFor="doctor_id">Select Doctor*</label>
                                                <select id="doctor_id" name="doctor_id" required value={ formData.doctor_id } onChange={ handleChange }>
                                                        <option value="">Choose a doctor</option>
                                                        { doctors.map( doctor => (
                                                                <option key={ doctor.id } value={ doctor.id }>
                                                                        { doctor.name } - { doctor.specialization }
                                                                </option>
                                                        ) ) }
                                                </select>
                                        </div>
                                        <div className="form-group">
                                                <label htmlFor="disease">Mention Your Disease</label>
                                                <textarea id="disease" name="disease" value={ formData.disease } onChange={ handleChange }></textarea>
                                        </div>
                                        <div className="button-group">
                                                <button type="submit">Book Appointment</button>
                                        </div>
                                </form>
                        </div>
                        <div className="image-container">
                                <img src="/img/front.jpg" alt="Medical Illustration" />
                        </div>
                        <Modal isOpen={ isModalOpen } onClose={ closeModal } message={ modalMessage } />
                </div>
        );
}

export default AppointmentForm;