//
//  ContentView.swift
//  SpaceApps
//
//  Created by Julia Holzbach on 10/4/25.
//

import SwiftUI

struct ContentView: View {
    
    let backgroundColor = Color(red: 96.0 / 255.0, green: 170.0 / 255.0, blue: 125.0 / 255.0)
    @State private var newPlants = false
    @State private var allDetails = false
    var body: some View {
        GeometryReader { geometry in
            NavigationView {
                ZStack {
                    TabView {
                        Tab("Home", systemImage: "house.fill") {
                            if(newPlants) {
                                AddNewPlants(newPlants: $newPlants)
                            }
                            else if(allDetails) {
                                ListOfPlants(newPlants: $newPlants, allDetails: $allDetails)
                            }
                            else {
                                Home(newPlants: $newPlants, allDetails: $allDetails)
                            }
                            //  else if(allDetails) {
                            //      PlantDetails(allDetails: $allDetails, plant: Fruit)
                            //  }
                            // else {
                            //     Home(newPlants: $newPlants, allDetails: $allDetails)
                            // }
                            //AbbrevListOfPlants(newPlants: $newPlants)
                        }
                        Tab("Model", systemImage: "globe.fill") {
                            Unity()
                        }
                        Tab("Community", systemImage: "tree.fill") {
                            Community()
                        }
                        
                    }
                    
                }
            }
        }
    }
}

#Preview {
    ContentView()
}
