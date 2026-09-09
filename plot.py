from dash import html, dcc, Output, Input, Dash, State
import time
import copy

UPDATE_FREQ = 190


class Plot:
    def __init__(self, controller):
        self.controller = controller
        self.state_fig = {
            "data": [
                {
                    "x": [],
                    "y": [],
                    "type": "scatter",
                    "mode": "lines",
                    "line": {"color": "#00ff66", "width": 2},  # Vibrant tech green line
                }
            ],
            "layout": {
                "paper_bgcolor": "#121212",  # Matches your body background
                "plot_bgcolor": "#121212",  # Dark plotting area
                "font": {"color": "white", "family": "Orbitron, sans-serif"},
                "yaxis": {
                    "range": [-self.controller.TARGET, self.controller.TARGET + 300],
                    "autorange": False,
                    "gridcolor": "#222222",  # Subtle tech grid lines
                    "zerolinecolor": "#444444",
                },
                "xaxis": {"gridcolor": "#222222", "zerolinecolor": "#444444"},
                "margin": {"l": 50, "r": 30, "t": 30, "b": 40},
            },
        }
        self.error_fig = copy.deepcopy(self.state_fig)
        self.error_fig["data"][0]["line"]["color"] = "#ff3333"
        self.error_fig["layout"]["yaxis"]["range"] = [-300, 300]

        self.start_time = time.perf_counter()
        self.time = self.start_time
        self.relative_time = 0

        self.loop_num = 0
        self.app = Dash()
        self.app.layout = html.Div(
            [
                html.Div(
                    id="title",
                    className="navbar",
                    children=[
                        html.Div(
                            [html.Img(src="/assets/mia.png")], className="nav-left"
                        ),
                        html.H1("MIA PID MONITOR", className="nav-center"),
                        html.Div(style={"width": "40px"}),
                    ],
                ),
                html.Div(
                    className="dashboard-container",
                    children=[
                        html.Div(
                            className = "graph-card",
                            children=[
                                html.H2("State Graph", className="sg_title"),
                                dcc.Graph(id="state_graph", figure=self.state_fig)
                            ]
                        ),
                        html.Div(
                            className = "graph-card",
                            children=[
                                html.H2("Error Graph", className="eg_title"),
                                dcc.Graph(id="error_graph", figure=self.error_fig)
                            ]
                        )
                    ]
                ),
                dcc.Interval(id="update", interval=UPDATE_FREQ),
            ]
        )
        self._register_callbacks()

    def _register_callbacks(self):
        @self.app.callback(
            Output("state_graph", "extendData"),
            Output("error_graph", "extendData"),
            Input("update", "n_intervals"),
        )
        def run_frame(interval):
            current_time = time.perf_counter()
            dt = current_time - self.time
            dt = max(0.01, dt)
            print(dt, "i am cute little dt")
            self.relative_time = current_time - self.start_time
            self.time = current_time

            current_error = self.controller.TARGET - self.controller.current_state
            error_dif = current_error - self.controller.error
            self.controller.error = current_error
            self.controller.accum_error += self.controller.error

            signal = self.controller.compute(dt, error_dif)
            self.controller.current_state += signal * 0.1

            print("_________________________________________________")
            print(
                f"Loop Number: {self.loop_num} -- Error : {self.controller.error} -- PID Out: {signal} --  State: {self.controller.current_state}"
            )
            print("_________________________________________________")
            self.loop_num += 1

            return (
                {"x": [[self.relative_time]], "y": [[self.controller.current_state]]},
                [0],
                100,
            ), (
                {"x": [[self.relative_time]], "y": [[self.controller.error]]},
                [0],
                100,
            )

    def begin(self):
        self.app.run(debug=True,port=8500)
