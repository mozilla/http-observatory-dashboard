$(document).ready(function() {
    'use strict';

    // initialize all the popovers
    $(function () { $('[data-toggle="popover"]').popover(
        {
            html: true,
            placement: 'top',
            trigger: 'hover'
        }
    ) });

});