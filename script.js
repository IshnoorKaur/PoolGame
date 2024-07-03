$(document).ready(function () {
    // Send an alert when the document is ready
    //alert("This is an alert from the script.js file!");

    function initializeEventHandlers() {
        // JavaScript code to select the cue ball
        cueBall = $('svg circle[fill="WHITE"]');
        cue = $('svg line');
        table = $('svg');
        isDrawing = false;
        let alertsShown = false;


        // Loop through each cue ball element and attach event listener
        $(this).on('mousedown', function (event) {
            isDrawing = true;

            cue.attr('x1', cueBall.attr("cx"));
            cue.attr('y1', cueBall.attr("cy"));
            cue.attr('x2', cueBall.attr("cx"));
            cue.attr('y2', cueBall.attr("cy"));
            cue.show();

        });

        // Event listener for mousemove to update the line
        $(document).on('mousemove', function (event) {
            if (!isDrawing) return;

            const { clientX, clientY } = event;
            const { left, top } = table.offset();

            const svgWidth = table.width();
            const svgHeight = table.height();
            const viewBoxWidth = 1400;
            const viewBoxHeight = 2750;

            const scaledX = ((clientX - left) / svgWidth) * viewBoxWidth;
            const scaledY = ((clientY - top) / svgHeight) * viewBoxHeight;

            cue.attr('x2', scaledX);
            cue.attr('y2', scaledY);
        });

        // Event listener for mouseup to remove the line and remove mousemove event listener
        $(document).on('mouseup', function (event) {
            if (isDrawing) {
                cue.hide();
                isDrawing = false;

                // Retrieve client coordinates of mouse release position
                const { clientX, clientY } = event;

                // Calculate scaled coordinates within the SVG viewBox
                const { left, top } = table.offset();
                const svgWidth = table.width();
                const svgHeight = table.height();
                const viewBoxWidth = 1400;
                const viewBoxHeight = 2750;

                const releaseX = ((clientX - left) / svgWidth) * viewBoxWidth;
                const releaseY = ((clientY - top) / svgHeight) * viewBoxHeight;

                // Retrieve cue ball position
                const cueBallX = (cueBall.attr("cx"));
                const cueBallY = (cueBall.attr("cy"));

                // Calculate the difference between cue ball position and release position
                const velx = (releaseX - cueBallX) * 4;
                const vely = (releaseY - cueBallY) * 4;
                // Show alert with initial velocity
                //alert(`Initial velocity:\nX: ${velx.toFixed(2)} mm/s\nY: ${vely.toFixed(2)} mm/s`);

                // Send POST request with initial velocity data
                $.post("shoot.html", JSON.stringify({
                    vel_x: velx.toString(),
                    vel_y: vely.toString()

                }),
                    function (res) {   //response headers 
                        let iteration = 0;

                        function processSVG() {
                            if (iteration < res.length) {
                                let item = res[iteration];

                                //Replace previous svg
                                $("svg").replaceWith(item);
                                initializeEventHandlers();
                                iteration++;

                                //Wait for some time before next information
                                setTimeout(processSVG, 10);
                            } else {
                                $.get("info",
                                    function (data) {
                                        console.log(data)
                                        const currentPlayer = data[0]
                                        const player1Assigned = data[1]
                                        const player2Assigned = data[2]
                                        const winner = data[3]

                                        console.log("Player 1 Balls:" + data[4])
                                        console.log("Player 2 Balls:" + data[5])

                                        // Show alerts for player balls only if not already shown
                                        if (!alertsShown && data[1] != null &&  data[2] != null) {
                                            alert("Player 1 Balls: " + data[1]);
                                            alert("Player 2 Balls: " + data[2]);
                                            alertsShown = true; // Set the flag to true to indicate that alerts have been shown
                                        }

                                        // Update player assigned information in HTML
                                        $("#player1Assigned").text(player1Assigned);
                                        $("#player2Assigned").text(player2Assigned);

                                        if (winner) {
                                            $("#winner").text("Winner: " + winner);
                                            // Send an alert if winner is not None
                                            if (winner !== "None") {
                                                alert("The winner is: " + winner);
                                                // Close the window
                                                window.close();
                                            }
                                        }
                                    })
                            };


                        }
                        function switchPlayer() {
                            $.ajax({
                                url: "/switch_player",
                                type: "POST",
                                success: function (response) {
                                    // Handle success if needed
                                    $(".current-player").text("Current Player: " + response);
                                    //alert("Player switched successfully");
                                },
                                error: function (xhr, status, error) {
                                    // Handle error if needed
                                    console.error("Error switching player:", error);
                                }
                            });
                        }
                        //start iterating
                        processSVG();
                        switchPlayer();
                    }
                );
            }
        });
    }

    initializeEventHandlers();
});
