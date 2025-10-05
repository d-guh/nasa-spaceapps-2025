//  ListOfPlants.swift
//  SpaceApps
//
//  Created by Julia Holzbach on 10/4/25.
//

import Foundation
import SwiftUI

private var plants: [Fruit] = [
   // Fruit(name: "Orange", growthToMaturity: 15, germinationTime: 4, pollinDate: 30, soilDepth: 1.5, waterFrequency: 2, status: .wait)
    Fruit(name: "Oranges", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 300),
    Fruit(name: "Almond", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 120)
]

let backgroundColor = Color(red: 160.0 / 255.0, green: 204.0 / 255.0, blue: 145.0 / 255.0)


//----------------------------------------------------------------------------------
struct ListOfPlants: View {
    
    //  let plantItem: Fruit
    @State var lists: [Fruit] = plants
    @Binding var newPlants: Bool
    @Binding var allDetails: Bool
    var body: some View {
        ZStack {
              //  Rectangle().fill(backgroundColor)
           
            VStack() {
        
                    ZStack {
                        RoundedRectangle(cornerRadius: 25).fill(backgroundColor).frame(height: 50)
                        HStack {
                            Button { allDetails.toggle() } label: {(Text("< Back")) }.padding(.trailing, 20).padding(.top, 10).padding(.bottom, 15).padding(.leading, 20).foregroundColor(Color.white)
                            
                          /*  Text("Your Plants:")
                                .font(.system(.headline, design: .rounded))
                                //.frame(maxWidth: .infinity, alignme)
                                .padding(.leading, 20)
                                .padding(.top, 10).padding(.bottom, 5)*/
                            
                            Button { newPlants.toggle() } label: { Text("Add Plants")}.frame(maxWidth: .infinity, alignment: .trailing).padding(.bottom, 5).padding(.bottom, 10).padding(.top, 10).padding(.trailing, 20).foregroundColor(Color.white)
                        }//Image(systemName: "plus.fill")
                }
              
               //     CalendarView()
                //        .padding(.top, 10)
                
                
                NavigationStack {
                        List {
                            
                            ForEach(plants) { plant in
                                NavigationLink(value: plant) {
                                    HStack {
                                        Text(plant.name)
                                            .padding(.leading)
                                        Spacer()
                                        Text("\(plant.status) |")
                                            .padding(.trailing)
                                    }
                                }
                            }
                        }
                        .navigationTitle("My Plants")
                        .navigationDestination(for: Fruit.self) { plant in
                            PlantDetails(plant: plant)
                        }
                            /*
                            ForEach(lists) { plant in
                                NavigationLink(destination: PlantDetails(plant: plant) {//allDetails: $allDetails) {
                                    HStack {
                                        Text(plant.name).padding(.leading)
                                        Spacer()
                                        Text("\(plant.status) |").padding(.trailing)
                                    }
                                }
                            }
                        }
                        .scrollContentBackground(.hidden)
                        .background(Color.blue.opacity(0.2))
                        .navigationBarBackButtonHidden()
                        //.navigationDestination(for: Fruit.self) { plant in
                            PlantDetails(allDetails: $allDetails, plant: plant)
                        }*/
                    }
                
                CalendarView()
                        .padding(.top, 10)
            }
        }
    }
}
            /*    NavigationStack {
                    List {
                        ForEach(lists) { plant in
                            NavigationLink(destination: PlantDetails(allDetails: $allDetails, plant: plant), isActive: $allDetails) {
                                HStack {
                                    Text(plant.name).padding(.leading)
                                    Spacer()
                                    Text("\(plant.status) |").padding(.trailing)
                                    //Text("\(plant.status) | \(plant.timeLeft) days").padding(.trailing)
                                }
                            }
                        }
                    }
                    .scrollContentBackground(.hidden)
                    .background(Color.blue.opacity(0.2))
                    .navigationBarBackButtonHidden()
                    .navigationDestination(for: Fruit.self) { plant in
                        PlantDetails(allDetails: $allDetails, plant: plant)
                    }
                }
            }*///.background(RoundedRectangle(cornerRadius: 15).fill(Color.yellow))
/*
    @Binding var newPlants: Bool
    @State var lists: [Fruit] = plants
    @Binding var allDetails: Bool
    
    var body: some View {
        ZStack {
            Spacer()
        
            VStack(spacing: 0){
                Spacer()
                HStack {
                    Text("Your Crops:")
                        .font(.system(.headline, design: .rounded))
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding(.leading, 20)
                        .padding(.top, 10)
                    Spacer()
                    
                    Button { newPlants.toggle() } label: {Image(systemName: "plus.circle.fill") }
                }.padding(.bottom, 10)
              
                NavigationStack {
                    List {
                        ForEach(lists) { plant in
                            NavigationLink(destination: PlantDetails(allDetails: $allDetails, plant: plant), isActive: $allDetails) {
                                HStack {
                                    Text(plant.name).padding(.leading)
                                    Spacer()
                                    Text("\(plant.status) |").padding(.trailing)
                                }
                            }
                        }
                    }
                    .scrollContentBackground(.hidden)
                    .background(Color.blue.opacity(0.2))
                    .navigationBarBackButtonHidden()
                   /* .safeAreaInset(edge: .bottom) {
                        Color.clear.frame(height: 50)
                    }*/
                    .navigationDestination(for: Fruit.self) { plant in
                        PlantDetails(allDetails: $allDetails, plant: plant)
                    }
                }
            }.background(RoundedRectangle(cornerRadius: 15).fill(backgroundColor))
        }
    }
}
*/

//----------------------------------------------------------------------------------
struct AddNewPlants: View {
    @Binding var newPlants: Bool
    @State var lists: [Fruit] = plants
    var body: some View {
        VStack {
            Button { newPlants.toggle() } label: {Image(systemName: "arrow.backward") }.padding().frame(maxWidth: .infinity, alignment: .leading)
            
            Text("Choose a plant to grow!").frame(maxWidth: .infinity, alignment: .leading).padding().font(.title).padding(.leading, 20)
            VStack {
            HStack {
                Button(action: {
                    plants.append(Fruit(name: "Strawberry", growthToMaturity: 30, plantDate: Date(), status: .wait, timeLeft: 20))
                }) {
                    ZStack {
                        RoundedRectangle(cornerRadius: 15).fill(.orange).frame(width:100, height: 100)
                        Image("Strawberry").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                    }
                }
                Button(action: {
                    plants.append(Fruit(name: "Orange", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 20))
                }) {
                    ZStack {
                        RoundedRectangle(cornerRadius: 15).fill(.indigo).frame(width:100, height: 100)
                        Image("Oranges").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                    }
                }
                Button(action: {
                    plants.append(Fruit(name: "Almond", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 20))
                }) {
                    ZStack {
                        RoundedRectangle(cornerRadius: 15).fill(.yellow).frame(width:100, height: 100)
                        Image("Almond").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                    }
                }
            }
            HStack {
                Button(action: {
                    plants.append(Fruit(name: "Grape", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 20))
                }) {
                    ZStack {
                        RoundedRectangle(cornerRadius: 15).fill(.red).frame(width:100, height: 100)
                        Image("Grape").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                    }
                }
                Button(action: {
                    plants.append(Fruit(name: "Lemon", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 20))
                }) {
                    ZStack {
                        RoundedRectangle(cornerRadius: 15).fill(.blue).frame(width:100, height: 100)
                        Image("Lemon").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                    }
                }
                Button(action: {
                    plants.append(Fruit(name: "Orange", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 20))
                }) {
                    ZStack {
                        RoundedRectangle(cornerRadius: 15).fill(.orange).frame(width:100, height: 100)
                        Image("Oranges").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                    }
                }
            }
                HStack {
                    Button(action: {
                        plants.append(Fruit(name: "Orange", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 20))
                    }) {
                        ZStack {
                            RoundedRectangle(cornerRadius: 15).fill(.teal).frame(width:100, height: 100)
                            Image("Oranges").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                        }
                    }
                    Button(action: {
                        plants.append(Fruit(name: "Orange", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 20))
                    }) {
                        ZStack {
                            RoundedRectangle(cornerRadius: 15).fill(.red).frame(width:100, height: 100)
                            Image("Oranges").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                        }
                    }
                    Button(action: {
                        plants.append(Fruit(name: "Orange", growthToMaturity: 180, plantDate: Date(), status: .wait, timeLeft: 20))
                    }) {
                        ZStack {
                            RoundedRectangle(cornerRadius: 15).fill(.orange).frame(width:100, height: 100)
                            Image("Oranges").resizable().scaledToFit().frame(width: 70, height: 70).padding(20)
                        }
                    }
                }
            }//.background(Color.blue).padding()
        }
    }
}


//----------------------------------------------------------------------------------
struct PlantDetails: View {
    // @Binding var allDetails: Bool
    let plant: Fruit
    var body: some View {
        VStack {
            HStack {
                Text(plant.name).frame(maxWidth: .infinity, alignment: .leading).font(.title).fontWeight(.bold).padding(.leading, 30)
                //.padding(.leading, 30)
                
                Image(plant.name).resizable().frame(width: 40, height: 40).padding(.trailing, 20)
            }
            Spacer()
            Text("Status: \(plant.status)").frame(maxWidth: .infinity, alignment: .leading).padding(.leading, 30).font(.subheadline).fontWeight(.bold)
            //Text("Details - ").frame(maxWidth: .infinity, alignment: .leading).padding(.leading, 30)
            Spacer()
            Text("Superblooms will occur in April, so plant accordingly.  Fruit will mature \(plant.growthToMaturity) days from planting.  You have \(plant.timeLeft) days until you should plant your \(plant.name)!").frame(maxWidth: .infinity, alignment: .leading).padding(.leading, 30)
            Spacer()
            if(plant.timeLeft < 100) {
                Text("Plant on: \(plant.plantDate)").frame(maxWidth: .infinity, alignment: .leading).padding(.leading, 30)
            }
            
            Spacer()
            
        }
        //Color(Color.blue.opacity(0.2)).ignoresSafeArea()
        /*
         
         ZStack {
         Color(Color.blue.opacity(0.2)).ignoresSafeArea()
         RoundedRectangle(cornerRadius: 15).fill(.white).padding()
         VStack {
         HStack {
         Text(plant.name).frame(maxWidth: .infinity, alignment: .trailing)
         .padding(.trailing, 5)
         .font(.system(.headline, design: .rounded))
         Image(plant.name).resizable().scaledToFit()//.clipShape(Circle())
         .frame(width: 30, height: 30)
         .padding(.trailing, 30)
         }
         Text("Status: \(plant.status)")
         .font(.system(.headline, design: .rounded))
         .frame(maxWidth: .infinity, alignment: .leading)
         .padding(.leading, 30)
         
         if(plant.status == .wait) {
         Text("\(plant.timeLeft) days until ready to plant")
         .frame(maxWidth: .infinity, alignment: .leading)
         .padding(.leading, 30)
         }
         if(plant.status == .plant) {
         Text("Time to plant!")
         .frame(maxWidth: .infinity, alignment: .leading)
         .padding(.leading, 30)
         Text("Instructions:")
         .frame(maxWidth: .infinity, alignment: .leading)
         .padding(.leading, 30)
         }
         
         if(plant.status == .grow) {
         Text("Growing!")
         .frame(maxWidth: .infinity, alignment: .leading)
         .padding(.leading, 30)
         Text("Reminders:")
         .frame(maxWidth: .infinity, alignment: .leading)
         .padding(.leading, 30)
         }
         }
         }
         }*/
    }
    
}
//----------------------------------------------------------------------------------
struct AbbrevListOfPlants: View {
    //  let plantItem: Fruit
    @State var lists: [Fruit] = plants
    @Binding var newPlants: Bool
    @Binding var allDetails: Bool
    var body: some View {
        ZStack {
            Spacer()
            
            
            VStack(spacing: 0) {
                Spacer()
                ZStack {
                    UnevenRoundedRectangle(
                        topLeadingRadius: 16, bottomLeadingRadius: 0, bottomTrailingRadius: 0, topTrailingRadius: 16, style: .continuous
                    ).fill(backgroundColor)
                    
                    HStack {
                        Text("Your Plants:")
                            .font(.system(.headline, design: .rounded))
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(.leading, 20)
                            .padding(.top, 10).padding(.bottom, 10)
                        Spacer()
                        
                        Button { allDetails.toggle() } label: {(Text("View All >")) }.padding(.trailing, 20).padding(.top, 10).padding(.bottom, 10)
                    }
                    
                }
                ZStack {
                    // Rectangle().fill(Color.blue.opacity(0.2))
                    UnevenRoundedRectangle(
                        topLeadingRadius: 0, bottomLeadingRadius: 16, bottomTrailingRadius: 16, topTrailingRadius: 0, style: .continuous
                    ).fill(Color.blue.opacity(0.2))
                    CalendarView()
                        .padding(.top, 10)
                }
            }
            /*    NavigationStack {
                    List {
                        ForEach(lists) { plant in
                            NavigationLink(destination: PlantDetails(allDetails: $allDetails, plant: plant), isActive: $allDetails) {
                                HStack {
                                    Text(plant.name).padding(.leading)
                                    Spacer()
                                    Text("\(plant.status) |").padding(.trailing)
                                    //Text("\(plant.status) | \(plant.timeLeft) days").padding(.trailing)
                                }
                            }
                        }
                    }
                    .scrollContentBackground(.hidden)
                    .background(Color.blue.opacity(0.2))
                    .navigationBarBackButtonHidden()
                    .navigationDestination(for: Fruit.self) { plant in
                        PlantDetails(allDetails: $allDetails, plant: plant)
                    }
                }
            }*///.background(RoundedRectangle(cornerRadius: 15).fill(Color.yellow))
        }
    }
}






//----------------------------------------------------------------------------------
/*struct Plant: Hashable, Identifiable {
    let name: String
    let timeLeft: Int
    var status: Status
    let id = UUID()
    
    enum Status {
        case wait
        case grow
        case plant
    }
}*/
/*
private var plants: [Plant] = [
    Plant(name: "Oranges", timeLeft: 10, status: .wait),
    Plant(name: "Strawberries", timeLeft: 10, status: .grow),
    Plant(name: "Melons", timeLeft: 10, status: .plant),
   // Plant(name: "Oranges", timeLeft: 10, status: "Harvest"),
   // Plant(name: "Strawberries", timeLeft: 10, status: "Harvest"),
   // Plant(name: "Melons", timeLeft: 10, status: "Harvest")
]

func addPlants() -> String {
    return "this"
}*/
