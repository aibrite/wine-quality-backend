//import {featureSet} from 'js/featureSet.js'
(function () {
    //var featureSet = [];
    var featureData = {};
    var sliders = [];
    var container;
    var rate;
    var featureSet = [{
        min: 1,
        max: 20,
        step: 0.01,
        name: 'alcohol0',
        friendlyName: 'Fixed Acidity',
        unit: 'ml',
        initialValue: 10.3
    },
    {
        min: 0.01,
        max: 2,
        step: 0.01,
        name: 'alcohol1',
        friendlyName: 'Volatile Acidity',
        unit: 'ml',
        initialValue: 0.32
    },
    {
        min: 0,
        max: 1.5,
        step: 0.01,
        name: 'alcohol2',
        friendlyName: 'Citric Acid',
        unit: 'ml',
        initialValue: 0.45
    },
    {
        min: 0.1,
        max: 20,
        step: 0.01,
        name: 'alcohol3',
        friendlyName: 'Residual Sugar',
        unit: 'ml',
        initialValue: 6.4
    },
    {
        min: 0.001,
        max: 1,
        step: 0.0001,
        name: 'alcohol4',
        friendlyName: 'Chlorides',
        unit: '%',
        initialValue: 0.073
    },
    {
        min: 1,
        max: 100,
        step: 0.1,
        name: 'alcohol5',
        friendlyName: 'Free Sulfur Dioxide',
        unit: '%',
        initialValue: 5
    },
    {
        min: 1,
        max: 400,
        step: 0.1,
        name: 'alcohol6',
        friendlyName: 'Total Sulfur Dioxide',
        unit: '%',
        initialValue: 13
    },
    {
        min: 0.1,
        max: 1.5,
        step: 0.001,
        name: 'alcohol7',
        friendlyName: 'Density',
        unit: '%',
        initialValue: 0.9976
    },
    {
        min: 0.1,
        max: 14,
        step: 0.01,
        name: 'alcohol8',
        friendlyName: 'pH',
        unit: '',
        initialValue: 3.23
    },
    {
        min: 0.1,
        max: 4,
        step: 0.01,
        name: 'alcohol9',
        friendlyName: 'Sulphates',
        unit: 'ml',
        initialValue: 0.82
    },
    {
        min: 4,
        max: 25,
        step: 0.1,
        name: 'alcohol10',
        friendlyName: 'Alcohol',
        unit: '%',
        initialValue: 12.6
    }]
    // var friendlyName = ['fixed acidity','volatile acidity','citric acid','residual sugar','chlorides','free sulfur dioxide','density','pH','total sulfur dioxid','sulphates','alcohol'];
    // var initialData = [7.4 , 0.7 , 0.03 , 1.9 , 0.076 , 11 , 34 , 0.9978 , 3.51 , 0.56 , 9.4];
    // var minData = [4.6, 0.12 , 0, 0.9 , 0.012 , 1 , 6 , 0.99007, 2.74 , 0.33 , 8.4];
    // var maxData = [15.9, 1.58, 1, 15.5, 0.611 , 72, 289,1.00369, 4.01 , 2, 14.9];

    postData = function () {
        $.post('https://wine-quality.herokuapp.com/predict', featureData, function (data, status) {
            console.log('Posting...')
        }).done(function (data, status) {
            console.log(data)
            //alert("Selected Wine Quality: " + data.prediction);
            $("#estimateQuality").rating("update", data.prediction);
            $(".quality-star").effect("shake", { times: 2 }, 1000);
            $('.loading-img').hide()
        }).fail(function (err) {
            console.log(err)
            $('.loading-img').hide()
            alert('Error. Please try again.')
        })
    }

    $(document).ready(function () {
        // $('.container').fadeIn(2000);
        // $('.container').slideDown(2000);
        $('.container').show(1500)
        postData()

    })

    for (var i = 0; i < 11; i++) {
        // featureSet.push({
        //     min: minData[i],
        //     max: maxData[i],
        //     step: 0.0001,
        //     name: 'alchohol' + i,
        //     friendlyName: friendlyName[i],
        //     unit: Math.random() > 0.5 ? 'ml' : '%',
        //     initialValue: 0.4 + (i / 100)
        // });

        featureData["alcohol" + i] = featureSet[i].initialValue;

    }

    document.addEventListener('DOMContentLoaded', function () {
        $('#rateQuality').rating({ min: 0, max: 100, step: 1, stars: 5 });
        $('#estimateQuality').rating({ displayOnly: true, min: 0, max: 10, step: 0.1, stars: 5 });
        container = document.querySelector('.sliders');
        createFatureEditors();
        $("#rateQuality").rating().on("rating.clear", function (event) {
            console.log("Your rating is reset")
        }).on("rating.change", function (event, value, caption) {
            $("#estimateQuality").rating("update", value / 10);
            console.log("You rated: " + value + " = " + $(caption).text());
            rate = value;
        });
    });

    var logToConsole = debounce(function () {
        console.log(featureData);

        //Utku: JQuery Server Call 
        postData()
    }, 2000, false)

    function createFatureEditors() {
        var sliderContainerTemplate = document.body.querySelector('#slider-template');
        featureSet.forEach(function (feature) {
            var featureEditor = document.createElement('input');
            featureEditor.type = 'range';
            featureEditor.min = feature.min;
            featureEditor.max = feature.max;
            featureEditor.step = feature.step;
            featureEditor.value = feature.initialValue;

            var sliderContainer = document.importNode(sliderContainerTemplate.content, true).querySelector('.cnt');
            sliderContainer.querySelector('.sliderContainer').appendChild(featureEditor);
            sliderContainer.querySelector('.footerText').innerHTML = feature.friendlyName;
            var headerText = sliderContainer.querySelector('.headerText');

            container.appendChild(sliderContainer);

            $(featureEditor).rangeslider({
                polyfill: false,
                orientation: 'vertical',
                onInit: function () {
                    this.boundProperty = feature.name;
                    this.setVal = function (value) {
                        setTimeout(function () {
                            this.$element.val(value).change();
                            this.$element.rangeslider('update', true);
                        }.bind(this))
                    }.bind(this);
                    this.setVal(featureData[this.boundProperty]);
                    sliders.push(this);
                },

                // Callback function
                onSlide: function (position, value) {
                    featureData[this.boundProperty] = value;
                    headerText.innerHTML = value + " " + feature.unit;
                },

                // Callback function
                onSlideEnd: function (position, value) {
                    $('.loading-img').show()

                    logToConsole();
                }
            });
        });
    }

    function updateSliders(data) {
        data = data || featureData;
        sliders.forEach((slider) => {
            slider.setVal(data[slider.boundProperty]);
        });
    }

    function debounce(func, wait, immediate) {
        var timeout;
        return function () {
            var context = this, args = arguments;
            var later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };

    window.wine = {
        update: updateSliders,
        data: featureData
    }
})();
