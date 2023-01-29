"use strict";

$(document).ready(() => {
    const review_form_element = $('#review_form').get(0);
    const root = ReactDOM.createRoot(review_form_element);
    console.log(review_form_element.dataset.dealerName);
    root.render(<ReviewForm dealerId={review_form_element.dataset.dealerId} formAction={review_form_element.dataset.formAction} dealerName={review_form_element.dataset.dealerName} />);
})

function ReviewForm(props) {

    const [review, set_review] = React.useState({
        content: "",
        car_purchased: false,
        car: "default",
        purchase_date: "",
    });

    const [dealership, set_dealership] = React.useState({
        cars: ""
    });

    const [validation, update_validation] = React.useState({
        error_content: false,
        error_car: false,
        error_purchase_date: false
    });

    React.useEffect(() => {
        fetch(`/djangoapp/details/${props.dealerId}`, {
            method: "GET",
            mode: "same-origin",
        })
            .then(res => {
                if (res.status === 200) {
                    res.json().then(data => {
                        set_dealership(() => {
                            return ({
                                cars: JSON.parse(data.cars)
                            });
                        })
                    });
                }
                else {
                    res.json().then(err => console.error(err["error"]))
                }
            })
            .catch(err => console.error(err));
    }, [props.dealerId]);

    const update_review = (event) => {
        const name = event.target.name;
        var value = null;
        if (name === "car_purchased") {
            value = event.target.checked;
        }
        else {
            value = event.target.value;
        }
        set_review(prev_state => {
            return ({
                ...prev_state,
                [name]: value
            })
        })
    };

    const submit_review = event => {
        event.preventDefault();
        fetch(props.formAction, {
            method: "POST",
            mode: "same-origin",
            body: JSON.stringify(review),
            headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
        })
            .then(res => {
                if (res.status === 200) {
                    window.location.assign(`/djangoapp/dealer/${props.dealerId}`);
                }
                else {
                    res.json().then(err => {
                        update_validation(() => {
                            return ({
                                error_content: err.result.error_content,
                                error_car: review.car_purchased ? err.result.error_car : false,
                                error_purchase_date: review.car_purchased ? err.result.error_purchase_date : false
                            });
                        });
                    });
                };
            })
            .catch(err => console.error(err));
    };

    return (
        <>
            <form className="form-control" onSubmit={submit_review}>
                <fieldset>
                    <div className="container">
                        <div className="row mb-4">
                            <div className="col">
                                <legend className="display-4 text-center">Add a review about {props.dealerName}</legend>
                            </div>
                        </div>
                        <div className="row mb-4">
                            <div className="col">
                                <label for="review" className="form-label mt-4">Enter the review content:</label>
                                <textarea name="content" className={`form-control ${validation.error_content ? 'is-invalid' : null}`} id="review" rows="3" spellcheck="false"
                                    value={review.content} onChange={update_review} required autoFocus></textarea>
                                {
                                    validation.error_content
                                        ?
                                        <div class="invalid-feedback">Please enter a valid review</div>
                                        :
                                        null
                                }
                            </div>
                        </div>
                        <div className="row mb-4">
                            <div className="col">
                                <input name="car_purchased" className="form-check-input me-2" type="checkbox"
                                    id="purchase_checkbox" checked={review.car_purchased} onChange={update_review} />
                                <label className="form-check-label" for="purchase_checkbox">
                                    Have you purchased a car from {props.dealerName}?
                                    <span className="text-muted">(Purchase information will be requested if checked)</span>
                                </label>
                            </div>
                        </div>
                        {
                            review.car_purchased
                                ?
                                <>
                                    <hr />
                                    <div className="row mb-4">
                                        <div className="col">
                                            <label for="car_select" className="form-label">Select you car (model-make-year)</label>
                                            <select name="car" className={`form-select ${validation.error_car ? 'is-invalid' : null}`} id="car_select" value={review.car} onChange={update_review} required>
                                                <option selected disabled value="default">Select</option>
                                                {dealership.cars && dealership.cars.map(car => {
                                                    return <Car key={car.pk} car={car} />
                                                })}
                                            </select>
                                            {
                                                validation.error_car
                                                    ?
                                                    <div class="invalid-feedback">Please select the purchased car</div>
                                                    :
                                                    null
                                            }
                                        </div>
                                    </div>
                                    <div className="row mb-2">
                                        <div className="col">
                                            <label className="col-form-label" for="purchase_date">Select Purchase Date</label>
                                            <input name="purchase_date" type="date" className={`form-control ${validation.error_purchase_date ? 'is-invalid' : null}`} id="purchase_date" value={review.purchase_date} onChange={update_review} required />
                                            {
                                                validation.error_purchase_date
                                                    ?
                                                    <div class="invalid-feedback">Please select a valid date of purchase</div>
                                                    :
                                                    null
                                            }
                                        </div>
                                    </div>
                                </>
                                :
                                null
                        }
                        <div className="row">
                            <div className="col">
                                <div class="d-grid">
                                    <button class="btn btn-primary" type="submit">Submit</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </fieldset>
            </form>
        </>
    );
};

function Car(props) {
    return (
        <>
            <option value={props.car.pk}>
                {props.car.fields.name}-{props.car.fields.car_make}-{new Date(props.car.fields.year).getFullYear()}
            </option>
        </>
    );
};