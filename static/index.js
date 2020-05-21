let factorsSelect = [];
let regionsSelect = [];
let yearsSelect = [];

$(document).ready(function () {
    getFactors();
    getRegions();
    getYears();
    //getCorrelMatrix();
    //drawBarchart();
    //drawLineChart();
    //drawTableForMatrix();
});

function getFactors() {
    let call = $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: '/api/getFactors',
        data: 'json',
        cache: false
    });

    call.done(function (data) {
        $.each(data, function (key, elem) {
            $('#factorLineSelect').append("<option value =" + elem + ">" + elem + "</option>");
            factorsSelect.push(elem);
        });
    });
}

function getRegions() {
    let call = $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: '/api/getRegions',
        data: 'json',
        cache: false
    });

    call.done(function (data) {
        $.each(data, function (key, elem) {
            $('.regionSelect').append("<option value =" + elem + ">" + elem + "</option>");
            regionsSelect.push(elem)
        })
    })
}

function getYears() {
    let call = $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: '/api/getYears',
        data: 'json',
        cache: false
    });

    call.done(function (data) {
        $.each(data, function (key, elem) {
            $('.yearsSelect').append("<option value =" + elem + ">" + elem + "</option>");
            yearsSelect.push(elem)
        })
    })
}

function getCorrelMatrix() {
    let selectedYear = $('#years').val();

    let call = $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: '/api/getData?year=' + selectedYear,
        data: 'json',
        cache: false
    });

    call.done(function (data) {
        let datas = [
            {
                z: data['corr'].reverse(),
                x: data['labels'],
                y: data['labels'].slice().reverse(),
                type: 'heatmap',
            }
        ];
        let layout = {
            title: 'Кореляційна матриця ',
            annotations: [],
            xaxis: {
                side: 'top'
            },
            yaxis: {
                side: 'left',
            }
        };

        Plotly.newPlot('myDiv', datas, layout);
    });
    call.fail(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    });

}

function drawTableForMatrix() {
    $('#correlMatrixTable').remove();
    $('.table-button').after("<table id=\"correlMatrixTable\" class=\"table\">\n" +
        "            <thead class=\"thead-row thead-dark\">\n" +
        "            </thead>\n" +
        "            <tbody class=\"tbody\">\n" +
        "\n" +
        "            </tbody>\n" +
        "        </table>");
    let selectedYear = $('#yearsExcel').val();

    let call = $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: '/api/getDataFromExcelByYear?year=' + selectedYear,
        cache: false
    });

    call.done(function (data) {
        let table_head = "<tr><td>Регіон</td>";

        $.each(data['table_header'], function (key, element) {
            table_head += "<td>" + element + "</td>";
        });
        table_head += "</tr>";

        $('.thead-row').append(table_head);

        $.each(data['table_data'], function (key, value) {
            let table_row = "<tr><td>" + key + "</td>"

            for (let i = 0; i < value.length; i++) {
                table_row += "<td>" + value[i] + "</td>"
            }
            table_row += "</tr>";
            $('.tbody').append(table_row);
        });

    });

    call.fail(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    });

}

function drawBarchart() {
    let year = $('#yearsBar').val();
    let factor = $('#factorBarSelect').val();
    let call = $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: '/api/getDataForBarChart?year=' + year + "&factor=" + factor,
        cache: false
    });

    call.done(function (data) {
        let datas = [
            {
                x: data['regions'],
                y: data['factors'],
                type: 'bar'
            }
        ];

        Plotly.newPlot('barChart', datas);
    });
    call.fail(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    });
}

function drawLineChart() {
    let factor = $('#factorLineSelect').val();
    let region = $('#regionLineSelect').val();
    let from = $('#yearsLineFrom').val();
    let to = $('#yearsLineTo').val();

    let call = $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: '/api/getDataForLineChart?from=' + from + "&to=" + to + "&factor=" + factor + "&region=" + region,
        cache: false
    });
    call.done(function (data) {
        let datas = [
            {
                x: data['years'],
                y: data['factor_in_years'],
                type: 'scatter'
            }
        ];

        Plotly.newPlot('lineChart', datas);
    });
    call.fail(function (jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    });
}



