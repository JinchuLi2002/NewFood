import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { feature, mesh } from 'topojson-client';

const USMap = ({ onSelectState }) => {
    const svgRef = useRef(null);
    const width = 960, height = 600;
    const stateIdToAbbreviation = {
        '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA',
        '08': 'CO', '09': 'CT', '10': 'DE', '11': 'DC', '12': 'FL',
        '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN',
        '19': 'IA', '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME',
        '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS',
        '29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH',
        '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND',
        '39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI',
        '45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT',
        '50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV', '55': 'WI',
        '56': 'WY'
    };
    useEffect(() => {
        const loadMapData = async () => {
            try {
                const us = await d3.json("https://d3js.org/us-10m.v2.json");
                const states = feature(us, us.objects.states).features;

                const svg = d3.select(svgRef.current)
                              .attr("viewBox", `0 0 ${width} ${height}`)
                              .style("width", "100%")
                              .style("height", "auto");

                const statePaths = svg.selectAll(".state")
                                      .data(states)
                                      .enter()
                                      .append("path")
                                      .attr("class", "state")
                                      .attr("d", d3.geoPath())
                                      .attr("fill", "#DFEBEB");

                statePaths.on("click", (event, d) => {
                    svg.selectAll(".state").attr("fill", "#DFEBEB"); // Reset all states' fill
                    d3.select(event.currentTarget).attr("fill", "#A8D1D1"); // Highlight selected state
                    const abbreviation = stateIdToAbbreviation[d.id]; // Get abbreviation from ID
                    onSelectState(abbreviation); // Pass both name and abbreviation
                    console.log(d.properties.name);
                    console.log(abbreviation);
                });

                svg.append("path")
                   .datum(mesh(us, us.objects.states, (a, b) => a !== b))
                   .attr("fill", "none")
                   .attr("stroke", "#97C1A9")
                   .attr("stroke-linejoin", "round")
                   .attr("d", d3.geoPath());
            } catch (error) {
                console.error("Error loading map data:", error);
            }
        };

        loadMapData();
    }, [onSelectState]);

    return <svg ref={svgRef}></svg>;
};

export default USMap;
