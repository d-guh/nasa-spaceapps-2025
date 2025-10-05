//
//  Home.swift
//  SpaceApps
//
//  Created by Julia Holzbach on 10/4/25.
//

import Foundation
import SwiftUI

struct Home: View {
    let backgroundColor = Color(red: 255.0 / 255.0, green: 229.0 / 255.0, blue: 196.0 / 255.0)
    let textColor = Color(red: 56.0 / 255.0, green: 34.0 / 255.0, blue: 12.0 / 255.0)
    @Binding var newPlants: Bool
    @Binding var allDetails: Bool
    
    
    var body: some View {
        ZStack {
            Color(backgroundColor).ignoresSafeArea()
            VStack {
                //  Spacer()
                Text("It's \"Grow\" Time!")
                    .font(.system(.largeTitle, design: .rounded))
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.leading, 20)
                    .padding(.top, 40)
                    .foregroundStyle(textColor)
                
                Image("Map").resizable().scaledToFit().cornerRadius(25).padding(.trailing, 15).padding(.leading, 15)
               /* GIFView(name: "ModelGif")
                    //.resizable()
                    .scaledToFit()
                    .frame(width: 100, height: 70)*/
                Text("Recent Trends Around the Globe").frame(maxWidth: .infinity, alignment: .trailing).padding(.trailing, 25)
                
                AbbrevListOfPlants(newPlants: $newPlants, allDetails: $allDetails)
                    .padding(15)
            }
        }
    }
}

