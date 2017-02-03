$(document).ready(function() {
    'use strict';

    // initialize all the popovers
    $(function () { $('.grade[data-toggle="popover"], a[data-toggle="popover"]').popover(
        {
            html: true,
            placement: 'top',
            trigger: 'hover'
        }
    ) });

    // the glyph info sign ones work a bit differently
    $(function () { $('.glyphicon-info-sign[data-toggle="popover"]').popover(
        {
            html: true,
            placement: 'bottom',
            trigger: 'click'
        }
    )});
});